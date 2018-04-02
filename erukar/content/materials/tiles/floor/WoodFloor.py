from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random, math

class WoodFloor(Tile):
    BaseAlias = 'wood flooring'

    generation_parameters = GenerationProfile(
        temperature = GenerationParameter(0.1),
        fabrication = GenerationParameter(0.5, dropoff=1.5),
        shelter     = GenerationParameter(0.3, dropoff=1.2),
        opulence    = GenerationParameter(-0.3)
    )

    def tile_id(self):
        return 'env-wood-floor'
    
    def generate(self, loc, total_dimensions):
        if loc[0] % 4:
            random_red = int(random.uniform(100, 130))
            random_green = int(random.uniform(80, 100))
            random_blue = int(random.uniform(35, 55))
        else:
            random_red = int(random.uniform(90, 110))
            random_green = int(random.uniform(50, 80))
            random_blue = int(random.uniform(0, 10))

        return [random_red,random_green,random_blue] + [1]
