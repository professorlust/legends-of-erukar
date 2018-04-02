from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class Cobblestone(Tile):
    BaseAlias = 'cobblestone'

    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.8),
        shelter     = GenerationParameter(0.3),
        opulence    = GenerationParameter(0.3)
    )

    def tile_id(self):
        return 'env-cobblestone'

    def generate(self, *_):
        random_gray = random.uniform(20, 130)
        return [int(random_gray) for x in range(3)] + [1]

