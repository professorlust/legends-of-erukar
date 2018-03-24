from .Lifeform import Lifeform
from erukar.system.engine import Indexer
from erukar.ext.math.Distance import Distance

class Player(Lifeform, Indexer):
    outline_pixels = [4,5,6,7,16,19,28,31,41,42,51,52,55,56,62,69,74,76,79,81,86,88,91,93,99,100,101,102,103,104,112,115,124,127,136,137,138,139]
    armor_pixels = [17,18,53,54,63,64,65,66,67,68,75,77,78,80,89,90,113,114,125,126]
    skin_pixels = [29,30,87,92]

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
        outline = {'r':32, 'g': 32, 'b': 32, 'a': 1}
        armor_color = {'r':158, 'g': 158, 'b': 158, 'a': 1}
        skin_tone = {'r': 160, 'g':108, 'b':89, 'a':1}

        for index in range(0, 144):
            if index in self.outline_pixels: yield outline
            elif index in self.armor_pixels: yield armor_color
            elif index in self.skin_pixels: yield skin_tone
            else: yield {'r':0, 'g':0, 'b':0, 'a':0}

    def generate_blob(self, dimensions):
        h, w = dimensions
        radius = int(w/3)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2),int(w/2))))
        inner_circle = list(Distance.points_in_circle(int(w/4)-1, (int(h/2),int(w/2))))
        for y in range(h):
            for x in range(w):
                if (x,y) in circle:
                    if (x,y) not in inner_circle:
                        yield {'r':0,'g':0,'b':0,'a':1}
                    else:
                        yield {'r':0,'g':255,'b':0,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}
