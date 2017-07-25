from erukar.engine.model.Tile import Tile
import random

class Grass(Tile):
    def generate(self, *_):
        random_red = int(random.uniform(20, 40))
        random_green = int(random.uniform(100, 150))
        random_blue = int(random.uniform(40, 80))
        return [random_red,random_green,random_blue] + [1]
