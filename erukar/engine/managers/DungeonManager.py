from erukar.engine.model.Manager import Manager

class DungeonManager(Manager):
    def __init__(self, dungeon):
        self.dungeon = dungeon 
        super().__init__()
