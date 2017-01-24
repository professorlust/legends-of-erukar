from erukar.server.Instance import Instance
from erukar.engine.factories import *
from erukar.engine.model.GenerationProfile import GenerationProfile
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

    def __init__(self, level=-1, level_variance=0.2, generation_properties=None, previous_identifier=''):
        super().__init__()
        self.level = level if level > 0 else int(random.uniform(1, 50))
        self.level_variance = level_variance
        if generation_properties is None:
            generation_properties = GenerationProfile.random()
        self.generation_parameters = generation_properties
        self.previous_identifier = previous_identifier

    def initialize_instance(self, action_commands, non_action_commands, sys_messages, responses):
        super().initialize_instance(action_commands, non_action_commands, sys_messages, responses)
        d = DungeonGenerator()
        self.dungeon = d.generate(self.previous_identifier)
        self.decorate()
        self.on_start()

    def decorate(self):
        decorators = list(self.decorators())
        # First Pass -- Actually add Decorations
        for room in self.dungeon.rooms:
            for deco in decorators:
                deco.apply_one_to(room)

    def decorators(self):
        for sm in RandomDungeonInstance.SubModules:
            md = sm[0](RandomDungeonInstance.BaseModule.format(sm[1]), self.generation_parameters)
            md.initialize()
            yield md

