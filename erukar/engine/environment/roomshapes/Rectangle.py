from .Shape import *

class Rectangle(Shape):
    '''Room Shape Decorator. Handles the drawing of a room in a map view.'''

    def coordinates(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        for x in range(2*room.width-1):
            for y in range(2*room.height-1):
                yield (x_i+x, y_i+y)
