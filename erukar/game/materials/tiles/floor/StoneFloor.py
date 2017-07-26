from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class StoneFloor(Tile):
    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.5, dropoff=1.5),
        shelter     = GenerationParameter(0.3, dropoff=1.2),
        opulence    = GenerationParameter(0.0)
    )

    def generate(self, *_):
        random_gray = random.uniform(100, 150)
        return [int(random_gray) for x in range(3)] + [1]

