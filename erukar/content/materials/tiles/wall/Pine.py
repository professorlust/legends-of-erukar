from erukar.system.engine import GenerationProfile, GenerationParameter, Tile
from ..floor.Grass import Grass
from erukar.ext.math.Distance import Distance
import random

class Pine(Tile):
    BaseAlias = 'a pine tree'
    
    generation_parameters = GenerationProfile(
        precipitation = GenerationParameter(1.0, strength=2),
        temperature = GenerationParameter(-0.8, dropoff=3, strength=2),
        fabrication = GenerationParameter(-0.5),
        shelter     = GenerationParameter(-1.0, dropoff=4.0)
    )

    def tile_id(self):
        return 'env-pine-tree'

    def build_generator(self, dimensions, *_):
        h, w = dimensions
        circles = list(Pine.get_circles(dimensions))
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

    def get_circles(dimensions):
        h, w = dimensions
        x0 = w/2
        y0 = h/2
        radius = int(w/2)
        for offset in [2,3,3]:
            radius -= offset
            x0 -= offset
            y0 += offset
            yield list(Distance.points_in_circle(radius, (x0, y0)))
