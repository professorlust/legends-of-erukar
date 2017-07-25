import random
from .Describable import Describable

class Tile(Describable):
    def __init__(self):
        super().__init__() 
    
    def generate(self, loc, total_dimensions):
        return 

    def rgba(r,g,b,a):
        return { 'r': r, 'g': g, 'b': b, 'a': a }
