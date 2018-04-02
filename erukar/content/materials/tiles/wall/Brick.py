from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class Brick(Tile):
    BaseAlias = 'a brick wall'

    def tile_id(self):
        return 'env-brick-wall'

    def generate(self, loc, total_dimensions):
        if (loc[1]+1) % 3 and (loc[1] + loc[0]) % 6:
            random_red = int(random.uniform(160, 180))
            random_green = int(random.uniform(40, 60))
            random_blue = int(random.uniform(1, 25))
        else: 
            random_red = int(random.uniform(160, 180))
            random_green = int(random.uniform(160, 180))
            random_blue = int(random.uniform(160, 180))
        return [random_red,random_green,random_blue] + [1]

