from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random, math

class WoodWall(Tile):

    def tile_id(self):
        return 'env-wood-wall'

    def generate(self, loc, total_dimensions):
        if loc[1] % 3:
            random_red = int(random.uniform(140, 160))
            random_green = int(random.uniform(100, 120))
            random_blue = int(random.uniform(40, 60))
        else:
            random_red = int(random.uniform(100, 120))
            random_green = int(random.uniform(60, 90))
            random_blue = int(random.uniform(0, 20))

        return [random_red,random_green,random_blue] + [1]

