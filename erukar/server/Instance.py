from erukar.data.Connector import Connector
from erukar.engine.factories import *
from erukar.engine.model.Manager import Manager
from erukar.server.TurnManager import TurnManager
from erukar.server.DataAccess import DataAccess
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
import erukar, threading

class Instance(Manager):
    MaximumTurnTime = 20.0 # In seconds
    MaximumTurnSkipPenalty = 5 # in turns
    BaseModule = "erukar.game.modifiers.room.{0}"
    SubModules = [
        (ModuleDecorator, "materials.floors"),
        (ModuleDecorator, "materials.walls"),
        (ModuleDecorator, "materials.ceilings"),
        (ModuleDecorator, "structure.ceilings"),
        (ModuleDecorator, "qualities.air"),
        (ModuleDecorator, "qualities.lighting"),
        (ModuleDecorator, "qualities.sounds"),
        (ModuleDecorator, "contents.enemies"),
        (MultipleModuleDecorator, "contents.decorations"),
        (ModuleDecorator, "contents.items"),
        (ModuleDecorator, "structure.passages"),
        (ModuleDecorator, "phenomena")]

    def __init__(self):
        super().__init__()
        self.command_contexts = {}

    def activate(self, action_commands, non_action_commands, joins, generation_parameters):
        '''Here generation_parameters is a GenerationProfile'''
        self.turn_manager = TurnManager()
        self.data = DataAccess()
        self.action_commands = action_commands
        self.non_action_commands = non_action_commands
        self.joins = joins
        d = DungeonGenerator()
        self.dungeon = d.generate()
        self.decorate(generation_parameters)
        self.subscribe_enemies()
        self.has_had_players = False

    def subscribe_enemies(self):
        for room in self.dungeon.rooms:
            for item in room.contents:
                if issubclass(type(item), erukar.engine.lifeforms.Enemy):
                    self.command_contexts[item.uid] = None
                    self.turn_manager.subscribe(item)
                    self.data.players.append(item)

    def decorate(self, generation_parameters):
        decorators = list(Instance.decorators(generation_parameters))
        self.generation_parameters = generation_parameters
        # First Pass -- Actually add Decorations
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)
        # Second pass -- Tell Decorators to start
        for room in self.dungeon.rooms:
            room.on_start()

    def decorators(gen_params):
        for sm in Instance.SubModules:
            md = sm[0](Instance.BaseModule.format(sm[1]), gen_params)
            md.initialize()
            yield md

    def subscribe(self, player):
        super().subscribe(player)
        p = self.launch_player(player.uid)
        room = self.dungeon.rooms[0]
        p.character.link_to_room(room)
        p.move_to_room(room)
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
        if not self.connector.load_player(uid, character):
            self.connector.add_character(uid, character)
            character.afflictions.append(erukar.engine.effects.NeedsInitialization(character, None))
        playernode.character = character
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
            if len(res) > 0:
                print(res)

        self.active_player = self.turn_manager.next()
        res = self.active_player.begin_turn()
        if len(res) > 0:
            print(res)

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
            if hasattr(result, 'result'):
                print(result.result + '\n')
            # Save Dirtied Characters in DB 
            if hasattr(result, 'dirtied_characters'):
                for dirty in result.dirtied_characters:
                    self.connector.update_character(dirty)
            # Set context for player
            self.command_contexts[cmd.sender_uid] = result
        return result
