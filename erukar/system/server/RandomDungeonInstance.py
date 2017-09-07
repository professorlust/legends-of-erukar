from .Instance import Instance
from erukar.system.engine import EnvironmentProfile, DungeonGenerator
import erukar

class RandomDungeonInstance(Instance):
    def __init__(self, location):
        super().__init__()
        self.location = location

    def initialize_instance(self, connector):
        super().initialize_instance(connector)
        d = DungeonGenerator(self.location)
        self.dungeon = d.generate()
        self.on_start()

    def handle_reduced_player_count(self):
        if len(self.characters) == 0:
            self.status = Instance.Closing
