from erukar.engine.factories import *
from erukar.engine.model.Manager import Manager
from erukar.server.TurnManager import TurnManager
from erukar.server.DataAccess import DataAccess
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
import erukar, threading

class Instance(Manager):
    MaximumTurnTime = 10.0 # In seconds
    MaximumTurnSkipPenalty = 5 # in turns
    BaseModule = "erukar.game.modifiers.room.{0}"
    SubModules = [
        "materials.floors",
        "materials.walls",
        "materials.ceilings",
        "structure.ceilings",
        "contents.enemies",
        "contents.decorations",
        "contents.items",
        "structure.passages",
        "phenomena",
        "qualities.air",
        "qualities.lighting",
        "qualities.sounds"]

    def activate(self, action_commands, non_action_commands,  generation_parameters):
        '''Here generation_parameters is a GenerationProfile'''
        self.turn_manager = TurnManager()
        self.data = DataAccess()
        self.action_commands = action_commands
        self.non_action_commands = non_action_commands
        d = DungeonGenerator()
        self.dungeon = d.generate()
        self.decorate(generation_parameters)
        self.subscribe_enemies()

    def subscribe_enemies(self):
        for room in self.dungeon.rooms:
            for item in room.contents:
                if issubclass(type(item), erukar.engine.lifeforms.Enemy):
                    self.turn_manager.subscribe(item)
    
    def decorate(self, generation_parameters):
        decorators = list(Instance.decorators(generation_parameters))
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)

    def decorators(gen_params):
        for sm in Instance.SubModules:
            yield ModuleDecorator(Instance.BaseModule.format(sm), gen_params)

    def subscribe(self, player):
        super().subscribe(player)
        p = self.create_player_node(player.uid)
        room = self.dungeon.rooms[0]
        p.character.link_to_room(room)
        p.move_to_room(room)
        self.turn_manager.subscribe(p)        

    def create_player_node(self, uid):
        character = Player()
        character.uid = uid
        character.define_stats({'dexterity': 20})
        p = PlayerNode(uid, character)
        self.data.players.append(p)
        return p
        
    def instance_running(self, action_commands, non_action_commands, gen_params):
        self.activate(action_commands, non_action_commands, gen_params)
        self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
        self.timer.start()
        self.active_player = None
        while True:
            if any(self.non_action_commands):
                # Run ALL of these
                cmd = self.non_action_commands.pop()
                self.execute_command(cmd)

            if isinstance(self.active_player, erukar.engine.model.PlayerNode):
                player_cmd = self.get_active_player_action()
                if player_cmd is None:
                    continue
                print(player_cmd)
                self.execute_command(player_cmd)

            if issubclass(type(self.active_player), erukar.engine.lifeforms.Enemy):
                self.active_player.perform_turn()

            self.active_player = self.turn_manager.next()
            self.timer.cancel()
            self.timer = threading.Timer(self.MaximumTurnTime, self.skip_player)
            self.timer.start()

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
        if isinstance(cmd, erukar.engine.commands.Join):
            self.subscribe(cmd.find_player())
        cmd.data = self.data
        result = cmd.execute()
        if result is not None:
            print(result + '\n')
