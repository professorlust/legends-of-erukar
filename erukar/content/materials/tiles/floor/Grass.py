from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class Grass(Tile):
    generation_parameters = GenerationProfile(
        ambient_water = GenerationParameter(0.5),
        precipitation = GenerationParameter(0.1),
        temperature = GenerationParameter(0.6),
        fertility = GenerationParameter(1.0, dropoff=1.5, strength=2),
        barrenness = GenerationParameter(-1.0, dropoff=0.5),
        altitude = GenerationParameter(0.3),
        fabrication = GenerationParameter(-0.2),
        shelter     = GenerationParameter(-1.0, dropoff=0.5)
    )

    def generate(self, *_):
        random_red = int(random.uniform(40, 60))
        random_green = int(random.uniform(120, 170))
        random_blue = int(random.uniform(20, 60))
        return [random_red,random_green,random_blue] + [1]