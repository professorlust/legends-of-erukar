from erukar.engine.factories import *
from erukar.engine.model.Manager import Manager
from erukar.engine.managers.TurnManager import TurnManager

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

    def __init__(self):
        super().__init__()
        self.turn_manager = TurnManager()

    def activate(self, generation_parameters):
        '''Here generation_parameters is a GenerationProfile'''
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
        self.turn_manager.subscribe(player)
