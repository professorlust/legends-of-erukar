from .Lifeform import Lifeform
from erukar.ext.math.Distance import Distance

class Npc(Lifeform):
    def __init__(self, templates=[]):
        super().__init__(None, "Npc")
        self.qualities = []
        for template in templates:
            template.apply(self)

    def generate_tile(self, dimensions):
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
                        yield {'r':0,'g':0,'b':255,'a':1}
                else: yield {'r':0,'g':0,'b':0,'a':0}


    def get_state(self):
        return {
            'type': 'Shop'
        }
