from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
from ..floor.Grass import Grass
from erukar.ext.math.Distance import Distance
import random

class Pine(Tile):
    generation_parameters = GenerationProfile(
        precipitation = GenerationParameter(1.0, strength=2),
        temperature = GenerationParameter(-0.8, dropoff=3, strength=2),
        fabrication = GenerationParameter(-0.5),
        shelter     = GenerationParameter(-1.0, dropoff=4.0)
    )

    def build_generator(self, dimensions):
        h, w = dimensions
        radius = int(w/2)-1
        circles = [list(Distance.points_in_circle(radius, (int(h/x)-(x-2),int(w/x)))) for x in [2,3,4]]
        for x in range(h):
            for y in range(w):
                scalar = sum((x,y) in circle for circle in circles)
                if not scalar:
                    random_red = int(random.uniform(1, 20))
                    random_green = int(random.uniform(35, 60))
                    random_blue = int(random.uniform(1, 10))
                else:
                    random_red = int(random.uniform(1, 30+20*scalar))
                    random_green = int(random.uniform(40+20*scalar, 70+23*scalar))
                    random_blue = int(random.uniform(5+20*scalar, 20+40*scalar))
                yield Tile.rgba(*[random_red, random_green, random_blue, 1.0])
