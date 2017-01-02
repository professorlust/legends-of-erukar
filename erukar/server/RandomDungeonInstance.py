from erukar.server.Instance import Instance
from erukar.engine.factories import *
import erukar

class RandomDungeonInstance(Instance):
    BaseModule = "erukar.game.modifiers.room.{0}"
    SubModules = [
        (ModuleDecorator, "materials.floors"),
        (ModuleDecorator, "materials.walls"),
        (ModuleDecorator, "materials.ceilings"),
        (ModuleDecorator, "structure.ceilings"),
        (ModuleDecorator, "qualities.air"),
        (ModuleDecorator, "qualities.sounds"),
        (ModuleDecorator, "contents.enemies"),
        (MultipleModuleDecorator, "contents.decorations"),
        (ModuleDecorator, "contents.items"),
        (ModuleDecorator, "structure.passages"),
        (ModuleDecorator, "phenomena")]

    def __init__(self, level=-1, level_variance=0.2, generation_parameters=None):
        self.level = level if level > 0 else int(random.uniform(1, 50))
        self.level_variance = level_variance
        if generation_parameters is None:
            generation_parameters = GenerationProfile.random()
        self.generation_parameters = generation_parameters

    def activate(self, action_commands, non_action_commands, joins):
        d = DungeonGenerator()
        self.dungeon = d.generate()
        self.decorate()
        super().activate(action_commands, non_action_commands, joins)

    def decorate(self):
        decorators = list(self.decorators(self.generation_parameters))
        # First Pass -- Actually add Decorations
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)

    def decorators(self):
        for sm in RandomDungeonInstance.SubModules:
            md = sm[0](RandomDungeonInstance.BaseModule.format(sm[1]), self.generation_parameters)
            md.initialize()
            yield md

