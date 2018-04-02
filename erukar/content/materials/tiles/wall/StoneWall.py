from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class StoneWall(Tile):
    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.5, dropoff=1.5),
        shelter     = GenerationParameter(0.3, dropoff=1.2),
        opulence    = GenerationParameter(0.0)
    )

    def tile_id(self):
        return 'env-stone-wall'

    def generate(self, *_):
        random_gray = random.uniform(130, 180)
        return [int(random_gray) for x in range(3)] + [1]
