from erukar.engine.model.Tile import Tile
import random

class StoneFloor(Tile):
    def generate(self, *_):
        random_gray = random.uniform(100, 150)
        return [int(random_gray) for x in range(3)] + [1]

