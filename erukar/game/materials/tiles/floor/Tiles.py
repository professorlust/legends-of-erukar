from erukar.engine.model.Tile import Tile
import random, math

class Tiles(Tile):
    def generate(self, loc, total_dimensions):
        if (loc[0] >= math.floor(total_dimensions[0]/2)) ^ (loc[1] >= math.floor(total_dimensions[1]/2)):
            random_red = int(random.uniform(200, 250))
            random_green = random_red
            random_blue = random_red
        else: 
            random_red = int(random.uniform(100, 150))
            random_green = random_red
            random_blue = random_red
        return [random_red,random_green,random_blue] + [1]
