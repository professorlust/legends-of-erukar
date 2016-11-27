from erukar.engine.model.Manager import Manager
from erukar.data.Connector import Connector
from erukar.server.TurnManager import TurnManager
from erukar.server.DataAccess import DataAccess
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
import erukar, threading

class Instance(Manager):
    MaximumTurnTime = 30.0 # In seconds
    MaximumTurnSkipPenalty = 5 # in turns

    def __init__(self):
        super().__init__()
        self.dungeon = None
        self.command_contexts = {}

    def activate(self, action_commands, non_action_commands, joins, generation_parameters):
        '''Here generation_parameters is a GenerationProfile'''
        self.turn_manager = TurnManager()
        self.data = DataAccess()
        self.action_commands = action_commands
        self.non_action_commands = non_action_commands
        self.joins = joins
        self.subscribe_enemies()
        self.has_had_players = False
        if self.dungeon:
            for room in self.dungeon.rooms:
                room.on_start()

    def subscribe_enemies(self):
        for room in self.dungeon.rooms:
            for item in room.contents:
                if issubclass(type(item), erukar.engine.lifeforms.Enemy):
                    self.command_contexts[item.uid] = None
                    self.turn_manager.subscribe(item)
                    self.data.players.append(item)

    def subscribe(self, player):
        super().subscribe(player)
        p = self.launch_player(player.uid)
        room = self.dungeon.rooms[0]
        p.character.link_to_room(room)
        p.move_to_room(room)
        # Run on_equip for all equipped items
        for equip in p.character.equipment_types:
            equipped = getattr(p.character, equip)
            if equipped is not None:
                equipped.on_equip(p.character)
        self.turn_manager.subscribe(p)
        self.command_contexts[player.uid] = None
        self.has_had_players = True

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
            character.afflictions.append(erukar.engine.effects.NeedsInitialization(character, None))
            self.connector.update_character(character)

        playernode.character = character
        character.spells = [
            erukar.game.magic.predefined.FlameBreath(),
            erukar.game.magic.predefined.Heal(),
            erukar.game.magic.predefined.AugmentWeapon()]
        self.data.players.append(playernode)
        return playernode

    def instance_running(self, connector, action_commands, non_action_commands, joins, gen_params):
        # Activate and initialize timers
        self.connector = connector
        self.activate(action_commands, non_action_commands, joins, gen_params)
        self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
        self.timer.start()
        self.active_player = None

        while not self.has_had_players or self.turn_manager.has_players():
            # Check for newly connecting players
            if any(self.joins):
                cmd = self.joins.pop()
                self.subscribe(cmd.find_player())

            # Check to see if our active Player exists and can send commands 
            if self.active_player is not None and not self.active_player.is_incapacitated():
                # run any non action command by any player
                if any(self.non_action_commands):
                    cmd = self.non_action_commands.pop()
                    self.execute_command(cmd)

                # if this is a player and not an AI, try to run an active command
                if isinstance(self.active_player, erukar.engine.model.PlayerNode):
                    player_cmd = self.get_active_player_action()
                    if player_cmd is None:
                        continue
                    result = self.execute_command(player_cmd)
                    if result is None or (result is not None and not result.success):
                        continue

                # If this is an AI, execute the command without worrying about failure
                if issubclass(type(self.active_player), erukar.engine.lifeforms.Enemy):
                    cmd = self.active_player.perform_turn()
                    if cmd is not None:
                        result = self.execute_command(cmd)

            # Get the next player and reset the timer
            self.get_next_player()
            self.timer.cancel()
            self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
            self.timer.start()

        print('No players, shutting down instance.')

    def get_next_player(self):
        if self.active_player is not None:
            res = self.active_player.end_turn()
            #TODO: Replace with Results object later
            if len(res) > 0:
                print(res)

        self.grab_from_turn_manager()
        if self.active_player is not None:
            res = self.active_player.begin_turn()
            #TODO: Same as above
            if len(res) > 0:
                print(res)

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
        print("Skipping player")
        for i in range(self.MaximumTurnSkipPenalty):
            next_player = self.turn_manager.next()
            if next_player is not self.active_player:
               break
        self.active_player = next_player

    def execute_command(self, cmd):
        cmd.context = self.command_contexts[cmd.sender_uid]
        cmd.data = self.data
        result = cmd.execute()

        # Check results
        if result is not None:
            # Print Result, replace with outbox later
            if hasattr(result, 'results'):
                if 'a-uid' in result.results:
                    print('\n\n'.join(result.result_for('a-uid')) + '\n')
                    print('-' * 64)

            # Save Dirtied Characters in DB 
            if hasattr(result, 'dirtied_characters'):
                for dirty in result.dirtied_characters:
                    self.connector.update_character(dirty)

            # Set context for player
            self.command_contexts[cmd.sender_uid] = result

        return result
