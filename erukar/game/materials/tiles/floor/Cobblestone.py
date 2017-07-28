from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class Cobblestone(Tile):
    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.8),
        shelter     = GenerationParameter(0.3),
        opulence    = GenerationParameter(0.3)
    )

    def generate(self, *_):
        random_gray = random.uniform(20, 130)
        return [int(random_gray) for x in range(3)] + [1]

