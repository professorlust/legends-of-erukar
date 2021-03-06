from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class StoneBricks(Tile):
    BaseAlias = 'a masoned stone wall'
    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.8),
        shelter     = GenerationParameter(0.3),
        opulence    = GenerationParameter(0.3)
    )

    def tile_id(self):
        return 'env-stone-brick-wall'

    def generate(self, loc, total_dimensions):
        if (loc[1]+1) % 3 and (loc[1] + loc[0]) % 6:
            random_gray = int(random.uniform(160, 180))
        else: 
            random_gray = int(random.uniform(130, 150))
        return [random_gray,random_gray,random_gray] + [1]
