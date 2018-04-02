from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class Dirt(Tile):
    BaseAlias = 'a patch of dirt'

    generation_parameters = GenerationProfile(
        precipitation = GenerationParameter(-0.2),
        ambient_water = GenerationParameter(-0.2),
        temperature = GenerationParameter(0.0),
        fertility = GenerationParameter(-0.8, dropoff=2.0),
        altitude = GenerationParameter(-0.1),
        fabrication = GenerationParameter(-0.8, dropoff=5.0),
        shelter     = GenerationParameter(-0.8, dropoff=2.0)
    )

    def tile_id(self):
        return 'env-dirt'

    def generate(self, *_):
        random_red = int(random.uniform(100, 150))
        random_green = int(random.uniform(60, 80))
        random_blue = int(random.uniform(00, 10))
        return [random_red,random_green,random_blue] + [1]

