from erukar.engine.model.Tile import Tile
import random

class Sand(Tile):
    def generate(self, *_):
        random_red = int(random.uniform(225, 250))
        random_green = int(random.uniform(180, 210))
        random_blue = int(random.uniform(170, 180))
        return [random_red,random_green,random_blue] + [1]


