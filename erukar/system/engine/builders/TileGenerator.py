from erukar.system.engine import Tile

class TileGenerator:
    def __init__(self, width, breadth):
        self.width = width
        self.breadth = breadth

    def build(self, tile):
        return list(self.build_generator(tile))

    def build_generator(self, tile):
        for y in range(self.breadth):
            for x in range(self.width):
                yield Tile.rgba(*tile.generate((x,y), (self.width, self.breadth)))
