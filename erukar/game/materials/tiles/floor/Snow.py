from erukar.engine.model.Tile import Tile
from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
import random, operator, functools

class Snow(Tile):
    generation_parameters = GenerationProfile(
        moisture = GenerationParameter(0.7, strength=1.2),
        temperature = GenerationParameter(-0.5, strength = 2),
        fabrication = GenerationParameter(-0.5),
        shelter     = GenerationParameter(-1.0, strength=4.0)
    )

    def generate(self, *_):
        random_gray = random.uniform(225, 250)
        return [int(random_gray) for x in range(3)] + [1]

