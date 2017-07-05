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
#       # Iterate over all of the rooms the player knows about
        results = {
            'minX': 0,
            'minY': 0,
            'height': 1,
            'width': 1,
            'rooms': [] # 
        }

        if not self.world:
            self.append_result(self.player_info.uid, results)
            return

        self.open_space = self.world.all_traversable_coordinates()

        # Now get the min and max range for x and y
        max_x, max_y = map(max, zip(*self.open_space))
        min_x, min_y = map(min, zip(*self.open_space))
        results['minX'] = min_x-1
        results['minY'] = min_y-1
        results['width'] = 3 + max_x - min_x
        results['height'] = 3 + max_y - min_y

        for y in range(min_y-1, max_y+2):
            for x in range(min_x-1, max_x+2):
                details = self.get_room_details(x, y)
                results['rooms'].append(details)
        self.append_result(self.player_info.uid, results)

    def get_room_details(self, x, y):
        return {
            'location': '{} {}'.format(x, y),
            'overlay': self.overlay_for(x,y),
            'layers': self.layers_for(x,y),
            'actions': self.actions_for(x, y)
        }

    def layers_for(self, x, y):
        result = ['cement']
        if (x,y) not in self.open_space:
            result.append('wood wall')
        result.append(self.world.moving_parts_at((x,y)))
        return result

    def actions_for(self, x, y):
        actions = {
            'Inspect': 2,
            'Glance': 1,
        }
        if any(coord == (x, y) for coord in self.open_space):
            actions['Move'] = 2
        return actions

    def overlay_for(self, x,y):
        return 'no overlay'
