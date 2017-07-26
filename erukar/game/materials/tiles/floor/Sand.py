from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class Sand(Tile):
    generation_parameters = GenerationProfile(
        moisture = GenerationParameter(-0.4),
        temperature = GenerationParameter(0.7),
        plant_growth = GenerationParameter(-1.0, strength=2.5),
        fabrication = GenerationParameter(-0.8, strength=2.0),
        shelter     = GenerationParameter(-1.0, strength=4.0)
    )

    def generate(self, *_):
        random_red = int(random.uniform(225, 250))
        random_green = int(random.uniform(180, 210))
        random_blue = int(random.uniform(170, 180))
        return [random_red,random_green,random_blue] + [1]


