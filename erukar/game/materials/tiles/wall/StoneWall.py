from erukar.engine.model.Tile import Tile
import random

class StoneWall(Tile):
    def generate(self, *_):
        random_gray = random.uniform(130, 180)
        return [int(random_gray) for x in range(3)] + [1]
