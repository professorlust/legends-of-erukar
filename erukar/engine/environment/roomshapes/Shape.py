from erukar.engine.commands.executable.Map import Map
import math

class Shape:
    '''Room Shape Decorator. Handles the drawing of a room in a map view.'''
    def center(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        mid_width = 2*round(room.width/2)
        mid_height = 2*round(room.height/2)
        return (x_i+mid_width, y_i+mid_height)

    def coordinates(room):
        pass
