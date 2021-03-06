from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class StoneFloor(Tile):
    BaseAlias = 'a stone floor'

    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.5, dropoff=1.5),
        shelter     = GenerationParameter(0.3, dropoff=1.2),
        opulence    = GenerationParameter(0.0)
    )

    def tile_id(self):
        return 'env-stone-floor'

    def generate(self, *_):
        random_gray = random.uniform(100, 150)
        return [int(random_gray) for x in range(3)] + [1]

