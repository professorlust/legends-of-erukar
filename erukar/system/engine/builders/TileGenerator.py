from erukar.system.engine import Tile

class TileGenerator:
    def __init__(self, width, breadth):
        self.width = width
        self.breadth = breadth

    def build(self, tile):
        return list(tile.build_generator((self.width, self.breadth)))

    def build_actor(self, actor):
        return list(actor.generate_tile((self.width, self.breadth)))
