from .Shape import *

class NorthEastCorner(Shape):
    def coordinates(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        x_corner = x_i + NorthEastCorner.x_corner_mod(room)
        y_corner = y_i + NorthEastCorner.y_corner_mod(room)
        for x in range(2*room.width-1):
            yield (x_i+x, y_corner)
        for y in range(2*room.height-1):
            yield (x_corner, y_i+y)

    def center(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        return (
            x_i + NorthEastCorner.x_corner_mod(room),
            y_i + NorthEastCorner.y_corner_mod(room)
        )

    def x_corner_mod(room):
        return 2*(room.width-1)

    def y_corner_mod(room):
        return 2*(room.height-1)
