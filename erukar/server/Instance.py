from erukar.engine.factories import *
from erukar.engine.model.Manager import Manager
from erukar.server.TurnManager import TurnManager
from erukar.server.DataAccess import DataAccess
from erukar.engine.lifeforms.Player import Player
from erukar.engine.model.PlayerNode import PlayerNode
import erukar, threading

class Instance(Manager):
    BaseModule = "erukar.game.modifiers.room.{0}"
    SubModules = [
        "materials.floors",
        "materials.walls",
        "materials.ceilings",
        "structure.ceilings",
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
        character.define_stats({'dexterity': 2})
        p = PlayerNode(uid, character)
        self.data.players.append(p)
        return p
        
    def instance_running(self, action_commands, non_action_commands, gen_params):
        self.activate(action_commands, non_action_commands, gen_params)
        while True:
            if any(self.non_action_commands):
                # Run ALL of these
                cmd = self.non_action_commands.pop()
                self.execute_command(cmd)
            if any(self.action_commands):
                # only run if turn order
                cmd = self.action_commands.pop()
                self.execute_command(cmd)

    def execute_command(self, cmd):
        if isinstance(cmd, erukar.engine.commands.Join):
            self.subscribe(cmd.find_player())
        cmd.data = self.data
        result = cmd.execute()
        if result is not None:
            print(result + '\n')
