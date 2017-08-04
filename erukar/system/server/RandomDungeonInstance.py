from .Instance import Instance
from erukar.system.engine import EnvironmentProfile, DungeonGenerator
import erukar

import logging
logger = logging.getLogger('debug')

class RandomDungeonInstance(Instance):
    def __init__(self, level=-1, level_variance=0.2, environment_profile=None, previous_identifier=''):
        super().__init__()
        self.level = level if level > 0 else int(random.uniform(1, 50))
        self.level_variance = level_variance
        if environment_profile is None:
            environment_profile = EnvironmentProfile.CityIndoors()
        self.environment_profile = environment_profile
        self.previous_identifier = previous_identifier

    def initialize_instance(self, connector):
        super().initialize_instance(connector)
        d = DungeonGenerator(self.environment_profile)
        self.dungeon = d.generate(self.previous_identifier)
        self.on_start()

    def handle_reduced_player_count(self):
        if len(self.characters) == 0:
            self.status = Instance.Closing
