from erukar.engine.model.GenerationProfile import GenerationProfile
from erukar.engine.model.GenerationParameter import GenerationParameter
from erukar.engine.model.Tile import Tile
import random

class StoneBricks(Tile):
    generation_parameters = GenerationProfile(
        fabrication = GenerationParameter(0.8),
        shelter     = GenerationParameter(0.3),
        opulence    = GenerationParameter(0.3)
    )

    def generate(self, loc, total_dimensions):
        if (loc[1]+1) % 2 and (loc[1] + loc[0]) % 4:
            random_gray = int(random.uniform(160, 180))
        else: 
            random_gray = int(random.uniform(130, 150))
        return [random_gray,random_gray,random_gray] + [1]
