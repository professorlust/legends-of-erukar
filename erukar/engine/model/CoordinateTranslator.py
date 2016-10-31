from erukar.engine.model import Direction

class CoordinateTranslator:
    def translate(origin_coord, direction):
        '''Hmm, how do I clean this up?'''
        x, y = origin_coord
        if direction is Direction.North:
            return (x, y+1)
        if direction is Direction.East:
            return (x+1, y)
        if direction is Direction.South:
            return (x, y-1)
        if direction is Direction.West:
            return (x-1, y)
        # Otherwise, just return the origin point... used when first generating
        return (0, 0)

    def translate_with_dimensions(origin_coord, dimensions, direction):
        x, y = origin_coord
        width, height = dimensions
        if direction is Direction.North:
            return (x, y+2*height-1)
        if direction is Direction.East:
            return (x+2*width-1, y)
        if direction is Direction.South:
            return (x, y-1)
        if direction is Direction.West:
            return (x-1, y)
        return (0,0)
