from erukar.system.engine import Tile

class TileGenerator:
    def __init__(self, dungeon=None, width=0, breadth=0):
        if dungeon:
            self.width = dungeon.pixels_per_side
            self.breadth = dungeon.pixels_per_side
            return
        self.width = width
        self.breadth = breadth

    def __init__dungeon(self, dungeon):
        self.width = dungeon.pixels_per_side,
        self.height = dungeon.pixels_per_side

    def build(self, tile):
        return list(tile.build_generator((self.width, self.breadth)))

    def build_actor(self, actor):
        return list(actor.generate_tile((self.width, self.breadth)))
