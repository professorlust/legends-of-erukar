from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.Command import Command
from erukar.engine.environment import *
from erukar.engine.model.CoordinateTranslator import CoordinateTranslator
from erukar.engine.model.Direction import Direction
import math

class Map(Command):
    NeedsArgs = False

    def perform(self, *_):
        '''Converts the dungeon_map into a readable map for the user'''
        self.dimensional_map()
        return self.succeed()

    def translate_coordinates_to_grid(coords):
        return tuple(map(lambda y: 2*y+1, coords))

    def translate_grid_to_coordinates(grid):
        return tuple(map(lambda y: int((y-1)/2), grid))

    def dimensional_map(self):
        self.open_space = []
#       self.dungeon = room.dungeon
#       # Iterate over all of the rooms the player knows about
        results = {
            'minX': 0,
            'minY': 0,
            'height': 1,
            'width': 1,
            'floors': [],
            'walls': [],
            'decor': [],
            'movingParts': [],
        }

        if not self.world:
            self.append_result(self.player_info.uid, results)
            return

        for room in self.world.rooms:
#           # Get a list of all coordinates which this room occupies
            room_coords = list(room.coordinates)
            self.open_space += room_coords
#       # Now get the min and max range for x and y
        max_x, max_y = map(max, zip(*self.open_space))
        min_x, min_y = map(min, zip(*self.open_space))
        results['minX'] = min_x-1
        results['minY'] = min_y-1
        results['width'] = 3 + max_x - min_x
        results['height'] = 3 + max_y - min_y
        for y in range(min_y-1, max_y+2):
            for x in range(min_x-1, max_x+2):
                results['floors'].append('cement')
                if (x,y) not in self.open_space:
                    results['walls'].append('wood wall')
                else: results['walls'].append('')
                results['decor'].append('')
                moving_parts_here = self.world.moving_parts_at((x,y))
                results['movingParts'].append(moving_parts_here)
        self.append_result(self.player_info.uid, results)

#   def should_draw_as_wall(self, coord):
#       '''This enforces the off-by-1 rule: only draw IFF next to open space'''
#       to_check = []
#       for x in range(-1,2):
#           for y in range(-1,2):
#               to_check.append((coord[0]+x, coord[1]+y))
#       return any(actual_room in to_check for actual_room in self.open_space)

#   def decode_door(passage):
#       '''Draws a door if it exists; then determines if open or closed'''
#       if not passage.door:
#           return Map.empty_space
#       if(passage.door.status is Door.Closed):
#           return Map.door_closed
#       return Map.door_open
