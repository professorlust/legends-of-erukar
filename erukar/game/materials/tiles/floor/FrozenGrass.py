from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class FrozenGrass(Tile):
    generation_parameters = GenerationProfile(
        moisture = GenerationParameter(0.3),
        temperature = GenerationParameter(-0.9, dropoff=4, strength=5),
        plant_growth = GenerationParameter(1.0, dropoff=1.5),
        barrenness = GenerationParameter(-0.8),
        altitude = GenerationParameter(0.3),
        fabrication = GenerationParameter(-0.2),
        shelter     = GenerationParameter(-1.0, dropoff=0.5)
    )

    def generate(self, *_):
        random_red = int(random.uniform(20, 40))
        random_green = int(random.uniform(80, 130))
        random_blue = int(random.uniform(60, 100))
        return [random_red,random_green,random_blue] + [1]
