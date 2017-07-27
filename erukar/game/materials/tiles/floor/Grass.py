from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class Grass(Tile):
    generation_parameters = GenerationProfile(
        ambient_water = GenerationParameter(0.3),
        precipitation = GenerationParameter(0.1),
        temperature = GenerationParameter(0.6, dropoff=4, strength=5.0),
        fertility = GenerationParameter(1.0, dropoff=1.5),
        altitude = GenerationParameter(0.3),
        fabrication = GenerationParameter(-0.2),
        shelter     = GenerationParameter(-1.0, dropoff=0.5)
    )

    def generate(self, *_):
        random_red = int(random.uniform(40, 60))
        random_green = int(random.uniform(120, 170))
        random_blue = int(random.uniform(20, 60))
        return [random_red,random_green,random_blue] + [1]
