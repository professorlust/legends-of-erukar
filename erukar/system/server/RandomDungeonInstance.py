from .Instance import Instance
from erukar.system.engine import EnvironmentProfile, DungeonGenerator
import erukar

class RandomDungeonInstance(Instance):
    def handle_reduced_player_count(self):
        if len(self.characters) == 0:
            self.status = Instance.Closing
