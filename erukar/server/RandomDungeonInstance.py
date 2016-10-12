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

    def activate(self, action_commands, non_action_commands, joins, generation_parameters):
        d = DungeonGenerator()
        self.dungeon = d.generate()
        self.decorate(generation_parameters)
        super().activate(action_commands, non_action_commands, joins, generation_parameters)

    def decorate(self, generation_parameters):
        decorators = list(RandomDungeonInstance.decorators(generation_parameters))
        self.generation_parameters = generation_parameters
        # First Pass -- Actually add Decorations
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)

    def decorators(gen_params):
        for sm in RandomDungeonInstance.SubModules:
            md = sm[0](RandomDungeonInstance.BaseModule.format(sm[1]), gen_params)
            md.initialize()
            yield md

