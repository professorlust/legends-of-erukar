from erukar.engine.model.Tile import Tile
from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
import random

class Dirt(Tile):
    generation_parameters = GenerationProfile(
        moisture = GenerationParameter(-0.2),
        temperature = GenerationParameter(0.0),
        plant_growth = GenerationParameter(-0.8, strength=2.0),
        altitude = GenerationParameter(-0.1),
        fabrication = GenerationParameter(-0.8, strength=5.0),
        shelter     = GenerationParameter(-0.8, strength=2.0)
    )

    def generate(self, *_):
        random_red = int(random.uniform(100, 150))
        random_green = int(random.uniform(60, 80))
        random_blue = int(random.uniform(00, 10))
        return [random_red,random_green,random_blue] + [1]

