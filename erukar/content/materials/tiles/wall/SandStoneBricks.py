from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class SandStoneBricks(Tile):
    generation_parameters = GenerationProfile(
        ambient_water = GenerationParameter(-0.2),
        precipitation = GenerationParameter(-0.7),
        temperature = GenerationParameter(0.7),
        fertility = GenerationParameter(-1.0, dropoff=2.5),
        fabrication = GenerationParameter(-0.8, dropoff=2.0),
        shelter     = GenerationParameter(-1.0, dropoff=4.0),
        barrenness = GenerationParameter(0.5),
    )

    def generate(self, loc, total_dimensions):
        if (loc[1]+1) % 2 and (loc[1] + loc[0]) % 4:
            random_red = int(random.uniform(210, 220))
            random_green = int(random.uniform(160, 180))
            random_blue = int(random.uniform(80, 100))
        else: 
            random_red = int(random.uniform(150, 190))
            random_green = int(random.uniform(120, 140))
            random_blue = int(random.uniform(60, 80))
        return [random_red,random_green,random_blue] + [1]
