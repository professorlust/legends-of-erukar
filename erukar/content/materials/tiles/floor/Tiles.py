from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random, math

class Tiles(Tile):
    generation_parameters = GenerationProfile(
        temperature = GenerationParameter(0.2),
        fabrication = GenerationParameter(1.0, dropoff=1.5),
        shelter     = GenerationParameter(1.0, dropoff=5),
        opulence    = GenerationParameter(0.8)
    )

    def tile_id(self):
        return 'env-tiled-floor'

    def generate(self, loc, total_dimensions):
        if (loc[0] >= math.floor(total_dimensions[0]/2)) ^ (loc[1] >= math.floor(total_dimensions[1]/2)):
            random_red = int(random.uniform(200, 250))
            random_green = random_red
            random_blue = random_red
        else: 
            random_red = int(random.uniform(50, 100))
            random_green = random_red
            random_blue = random_red
        return [random_red,random_green,random_blue] + [1]
