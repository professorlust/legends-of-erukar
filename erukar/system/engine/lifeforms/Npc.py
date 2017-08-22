from .Lifeform import Lifeform

class Npc(Lifeform):
    def __init__(self, templates=[]):
        super().__init__()
        self.qualities = []
        for template in templates:
            template.apply(self)

    def generate_tile(self, dimensions):
        h, w = dimensions
        radius = int(w/2)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2),int(w/2))))
        for y in range(h):
            for x in range(w):
                if (x,y) in circle:
                    yield {'r':0,'g':0,'b':255,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}

