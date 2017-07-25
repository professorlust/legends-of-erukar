from erukar.engine.model.Tile import Tile
import random, math

class WoodFloor(Tile):
    def generate(self, loc, total_dimensions):
        if loc[0] % 3:
            random_red = int(random.uniform(100, 130))
            random_green = int(random.uniform(80, 100))
            random_blue = int(random.uniform(35, 55))
        else:
            random_red = int(random.uniform(90, 110))
            random_green = int(random.uniform(50, 80))
            random_blue = int(random.uniform(0, 10))

        return [random_red,random_green,random_blue] + [1]
