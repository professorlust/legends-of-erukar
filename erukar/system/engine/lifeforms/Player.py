from erukar.system.engine import Indexer
from .Lifeform import Lifeform
from erukar.ext.math.Distance import Distance

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

    def generate_tile(self, dimensions):
        h, w = dimensions
        radius = int(w/2)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2),int(w/2))))
        for y in range(h):
            for x in range(w):
                if (x,y) in circle:
                    yield {'r':0,'g':255,'b':0,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}

