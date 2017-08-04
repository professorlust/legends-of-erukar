from .Describable import Describable
import random

class Tile(Describable):
    def __init__(self):
        super().__init__() 
    
    def generate(self, loc, total_dimensions):
        return 

    def rgba(r,g,b,a):
        return { 'r': r, 'g': g, 'b': b, 'a': a }

    def build_generator(self, dimensions):
        w, h = dimensions 
        for y in range(h):
            for x in range(w):
                yield Tile.rgba(*self.generate((x,y), (w, h)))
