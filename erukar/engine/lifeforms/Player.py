from erukar.engine.model.Indexer import Indexer
from erukar.engine.lifeforms.Lifeform import Lifeform

class Player(Lifeform, Indexer):
    def __init__(self):
        Indexer.__init__(self)
        super().__init__()
        self.uid = '' # Player UID
        self.credits = 0
        self.define_level(1)

    def alias(self):
        return self.uid

    def lifeform(self):
        return self
