from erukar.engine.model.Manager import Manager
from erukar.data.Connector import Connector
from erukar.server.TurnManager import TurnManager
from erukar.server.DataAccess import DataAccess
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
import erukar, threading, random

class Instance(Manager):
    MaximumTurnTime = 30.0 # In seconds
    MaximumTurnSkipPenalty = 5 # in turns
    TickRate = 0.2 # in seconds

    def __init__(self):
        super().__init__()
        self.active_player = None
        self.properties = None
        self.identifier = 'n/a'
        self.dungeon = None
        self.command_contexts = {}

    def instance_running(self, connector, action_commands, non_action_commands, sys_messages, responses):
        '''Entry point for the Initialization of the Instance by the Shard'''
        # Activate and initialize timers
        self.connector = connector
        self.initialize_instance(action_commands, non_action_commands, sys_messages, responses)
        self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
        self.timer.start()
        self.check_for_player_input()

    def initialize_instance(self, action_commands, non_action_commands, sys_messages, responses):
        '''Turn on players and generate a dungeon'''
        self.turn_manager = TurnManager()
        self.data = DataAccess()
        self.action_commands = action_commands
        self.non_action_commands = non_action_commands
        self.sys_messages = sys_messages
        self.responses = responses
        if self.dungeon:
            self.on_start()

    def on_start(self):
        self.subscribe_enemies()
        for room in self.dungeon.rooms:
            room.on_start()

    def any_connected_players(self):
        '''Check to see if there are any currently connected players'''
        return any([isinstance(x, PlayerNode) for x in self.data.players])

    def subscribe_enemies(self):
        for room in self.dungeon.rooms:
            for item in room.contents:
                self.handle_enemy_persistence(room, item)
            room.contents = [c for c in room.contents if not (isinstance(type(c), erukar.engine.lifeforms.Enemy) and c.requesting_persisted)]

    def handle_enemy_persistence(self, room, enemy):
        '''Get persisted enemies where available'''
        if not issubclass(type(enemy), erukar.engine.lifeforms.Enemy):
            return

        if enemy.requesting_persisted:
            persisted_enemy = self.try_to_get_persistent_enemy(enemy)
            if persisted_enemy:
                persisted_enemy.link_to_room(room)
                persisted_enemy.is_transient = False
                self.subscribe_enemy(persisted_enemy)
            return

        self.subscribe_enemy(enemy)

    def subscribe_enemy(self, enemy):
        enemy.subscribe(self)
        self.command_contexts[enemy.uid] = None
        self.turn_manager.subscribe(enemy)
        self.data.players.append(enemy)

    def unsubscribe(self, player):
        self.turn_manager.unsubscribe(player)
        self.data.players.remove(player)
        super().unsubscribe(player)
        player.lifeform().transition_properties.previous_identifier = self.identifier
        self.sys_messages[player.uid] = player.lifeform().transition_properties 

    def try_to_get_persistent_enemy(self, enemy):
        possible_uids = [e.uid for e in self.connector.get_creature_uids() if not self.data.find_player(e.uid)]
        if len(possible_uids) <= 0: 
            return
        uid = random.choice(possible_uids)
        return self.connector.load_creature(uid)

    def subscribe(self, uid):
        prejoin = self.any_connected_players()
        player = self.launch_player(uid)
        super().subscribe(player)
        room = self.dungeon.rooms[0]
        player.character.link_to_room(room)
        player.character.subscribe(self)
        player.move_to_room(room)
        # Run on_equip for all equipped items
        for equip in player.character.equipment_types:
            equipped = getattr(player.character, equip)
            if equipped is not None:
                equipped.on_equip(player.character)
        self.turn_manager.subscribe(player)
        self.command_contexts[uid] = None
        if not prejoin:
            self.get_next_player()

    def launch_player(self, uid):
        # Create the base object
        character = Player()
        playernode = self.connector.get_player({'uid': uid})
        if playernode is None:
            playernode = PlayerNode(uid)
            self.connector.add_player(playernode)
        character.uid = uid

        # If this is a new character, mark it for Initialization
        if not self.connector.load_player(uid, character):
            self.connector.add_character(uid, character)
            self.connector.update_character(character)

        playernode.character = character
        self.data.players.append(playernode)
        return playernode

    def check_for_player_input(self):
        if any(self.non_action_commands):
            cmd = self.non_action_commands.pop()
            self.execute_command(cmd)

        if self.any_connected_players():
            self.execute_player_turn()

        self.timer.cancel()
        self.timer = threading.Timer(self.TickRate, self.check_for_player_input)
        self.timer.start()

    def execute_player_turn(self):
        if isinstance(self.active_player, erukar.engine.model.PlayerNode):
            player_cmd = self.get_active_player_action()
            if player_cmd is None:
                return
            result = self.execute_command(player_cmd)
            if result is None or (result is not None and not result.success):
                return

            self.get_next_player()

        # Go ahead and execute ai turns
        while self.turn_manager.has_players() and issubclass(type(self.active_player), erukar.engine.lifeforms.Enemy):
            if not self.active_player.is_incapacitated():
                self.execute_ai_turn()
            self.get_next_player()

        self.timer.cancel()
        self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
        self.timer.start()

    def execute_ai_turn(self):
        cmd = self.active_player.perform_turn()
        if cmd is not None:
            result = self.execute_command(cmd)

    def get_next_player(self):
        if self.active_player is not None:
            res = self.active_player.end_turn()
            #TODO: Replace with Results object later
            if len(res) > 0:
                self.append_response(self.active_player.uid, res)

        self.grab_from_turn_manager()
        if self.active_player is not None:
            res = self.active_player.begin_turn()
            #TODO: Same as above
            if len(res) > 0:
                self.append_response(self.active_player.uid, res)

    def grab_from_turn_manager(self):
        self.active_player = self.turn_manager.next()
        if self.turn_manager.needs_tick():
            self.dungeon.tick()
            for player in self.data.players:
                player.lifeform().tick()

    def get_active_player_action(self):
        for command in self.action_commands:
            if command.sender_uid == self.active_player.uid:
                while len(self.action_commands) > 0:
                    self.action_commands.pop()
                return command

    def skip_player(self):
        self.append_response(self.active_player.uid, 'You were skipped!')
        for i in range(self.MaximumTurnSkipPenalty):
            next_player = self.turn_manager.next()
            if next_player is not self.active_player:
               break
        self.active_player = next_player

    def execute_command(self, cmd):
        cmd.server_properties = self.properties
        cmd.context = self.command_contexts[cmd.sender_uid]
        cmd.data = self.data
        if cmd.context and not hasattr(cmd.context, 'server_properties'):
            cmd.context.server_properties = self.properties
        result = cmd.execute()

        # Check results
        if result is not None:
            # Print Result, replace with outbox later
            if hasattr(result, 'results'):
                self.append_result_responses(result)

            # Save Dirtied Characters in DB 
            if hasattr(result, 'dirtied_characters'):
                for dirty in result.dirtied_characters:
                    self.connector.update_character(dirty)

            # Set context for player
            self.command_contexts[cmd.sender_uid] = result

        self.check_for_transitions(result)
        return result

    def check_for_transitions(self, result):
        for player in self.data.players:
            if hasattr(player.lifeform(), 'transition_properties') and player.lifeform().transition_properties is not None:
                self.unsubscribe(player)

    def append_result_responses(self, result):
        for uid in result.results:
            self.append_response(uid,'\n'.join(result.result_for(uid)) + '\n')

    def append_response(self, uid, response):
        if uid not in self.responses:
            self.responses[uid] = [response]
            return
        self.responses[uid] = self.responses[uid] + [response]
