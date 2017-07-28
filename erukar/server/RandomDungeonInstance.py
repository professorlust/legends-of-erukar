from erukar.server.Instance import Instance
from erukar.engine.factories import *
from erukar.engine.model.EnvironmentProfile import EnvironmentProfile
import erukar

import logging
logger = logging.getLogger('debug')

class RandomDungeonInstance(Instance):
    BaseModule = "erukar.game.modifiers.room.{0}"
    SubModules = []
#       (ModuleDecorator, "materials.floors"),
#       (ModuleDecorator, "materials.walls"),
#       (ModuleDecorator, "materials.ceilings"),
#       (ModuleDecorator, "structure.ceilings"),
#       (ModuleDecorator, "qualities.air"),
#       (ModuleDecorator, "qualities.sounds"),
#       #(ModuleDecorator, "contents.enemies"),
#       (MultipleModuleDecorator, "contents.decorations"),
#       (ModuleDecorator, "contents.items"),
#       (ModuleDecorator, "structure.passages"),
#       (ModuleDecorator, "phenomena")]

    def __init__(self, level=-1, level_variance=0.2, environment_profile=None, previous_identifier=''):
        super().__init__()
        self.level = level if level > 0 else int(random.uniform(1, 50))
        self.level_variance = level_variance
        if environment_profile is None:
            environment_profile = EnvironmentProfile.CityOutdoors()
        self.environment_profile = environment_profile
        self.previous_identifier = previous_identifier

    def initialize_instance(self, connector):
        super().initialize_instance(connector)
        d = DungeonGeneratorRedux(self.environment_profile)
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
            md = sm[0](RandomDungeonInstance.BaseModule.format(sm[1]), self.environment_profile)
            yield md

    def handle_reduced_player_count(self):
        if len(self.characters) == 0:
            self.status = Instance.Closing
