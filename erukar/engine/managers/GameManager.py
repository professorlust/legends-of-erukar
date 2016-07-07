from erukar.engine.model.Manager import Manager
from erukar.engine.managers.DungeonManager import DungeonManager

class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self.dungeons = []

    def generate_dungeon(self):
        pass

    def subscribe(self, player):
        super().subscribe(player)
        for dungeon in self.dungeons:
            dungeon.subscribe(player)
