import random

class TileGenerator:
    def __init__(self, width, breadth):
        self.width = width
        self.breadth = breadth

    def build(self, tile):
        return list(self.build_generator(tile))

    def build_generator(self, tile):
        for pixel in range(self.width*self.breadth):
            if tile == 'wall':
                yield TileGenerator.rgba(*TileGenerator.random_wall())
            else:
                yield TileGenerator.rgba(*TileGenerator.random_floor())

    def rgba(r,g,b,a):
        return { 'r': r, 'g': g, 'b': b, 'a': a }

    def random_wall():
        random_gray = random.uniform(100, 150)
        return [int(random_gray) for x in range(3)] + [1]

    def random_floor():
        random_red = int(random.uniform(20, 40))
        random_green = int(random.uniform(100, 150))
        random_blue = int(random.uniform(40, 80))
        return [random_red,random_green,random_blue] + [1]
