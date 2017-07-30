from erukar.system.engine import Indexer
from .Lifeform import Lifeform

class Player(Lifeform, Indexer):
    def __init__(self, world=None):
        Indexer.__init__(self)
        super().__init__(world)
        self.uid = '' # Player UID
        self.credits = 0
        self.define_level(1)

    def alias(self):
        return self.uid

    def lifeform(self):
        return self
