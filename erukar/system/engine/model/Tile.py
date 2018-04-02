from .Describable import Describable
import random

class Tile(Describable):
    BaseAlias = 'A tile'

    def __init__(self):
        super().__init__() 
    
    def generate(self, loc, total_dimensions):
        return 

    def rgba(r,g,b,a):
        return { 'r': r, 'g': g, 'b': b, 'a': a }

    def tile_id(self):
        return str(self.uuid)

    def ids_to_generate(self):
        return [self.tile_id()]

    def build_generator(self, dimensions, tile_id):
        w, h = dimensions 
        for y in range(h):
            for x in range(w):
                yield Tile.rgba(*self.generate((x,y), (w, h)))

    def alias(self):
        return self.BaseAlias
