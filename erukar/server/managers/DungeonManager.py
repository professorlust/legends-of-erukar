from erukar.engine.factories import *
from erukar.engine.model.Manager import Manager
from erukar.server.managers.TurnManager import TurnManager

class DungeonManager(Manager):
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

    def activate(self, requests,  generation_parameters):
        '''Here generation_parameters is a GenerationProfile'''
        self.turn_manager = TurnManager()
        self.requests = requests
        d = DungeonGenerator()
        self.dungeon = d.generate()
        self.decorate(generation_parameters)
    
    def decorate(self, generation_parameters):
        decorators = list(DungeonManager.decorators(generation_parameters))
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)

    def decorators(gen_params):
        for sm in DungeonManager.SubModules:
            yield ModuleDecorator(DungeonManager.BaseModule.format(sm), gen_params)

    def subscribe(self, player):
        super().subscribe(player)
        room = self.dungeon.rooms[0]
        player.character.link_to_room(room)
        player.move_to_room(room)
        self.turn_manager.subscribe(player)        
        
    def instance_running(self, requests, gen_params):
        self.activate(requests, gen_params)
        while True:
            if any(self.requests):
                cmd = self.requests.pop()
                print(cmd.execute())
