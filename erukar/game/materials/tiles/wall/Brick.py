from erukar.engine.model.Tile import Tile
import random

class Brick(Tile):
    def generate(self, loc, total_dimensions):
        if (loc[1]+1) % 2 and (loc[1] + loc[0]) % 4:
            random_red = int(random.uniform(160, 180))
            random_green = int(random.uniform(40, 60))
            random_blue = int(random.uniform(1, 25))
        else: 
            random_red = int(random.uniform(160, 180))
            random_green = int(random.uniform(160, 180))
            random_blue = int(random.uniform(160, 180))
        return [random_red,random_green,random_blue] + [1]

