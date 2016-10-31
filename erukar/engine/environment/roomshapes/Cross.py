from .Shape import *

class Cross(Shape):
    '''Room Shape Decorator. Handles the drawing of a room in a map view.'''

    def coordinates(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        mid_width = round(room.width/2)
        mid_height = round(room.height/2)
        for x in range(2*room.width-1):
            yield (x_i+x, y_i+mid_height)
        for y in range(2*room.height-1):
            yield (x_i+mid_width, y_i+y)

