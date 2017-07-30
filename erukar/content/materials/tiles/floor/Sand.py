from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
import random

class Sand(Tile):
    generation_parameters = GenerationProfile(
        ambient_water = GenerationParameter(-0.2),
        precipitation = GenerationParameter(-0.7),
        temperature = GenerationParameter(0.7),
        fertility = GenerationParameter(-1.0, dropoff=2.5),
        fabrication = GenerationParameter(-0.8, dropoff=2.0),
        shelter     = GenerationParameter(-1.0, dropoff=4.0),
        barrenness = GenerationParameter(0.5),
    )

    def generate(self, *_):
        random_red = int(random.uniform(210, 220))
        random_green = int(random.uniform(160, 180))
        random_blue = int(random.uniform(80, 100))
        return [random_red,random_green,random_blue] + [1]


