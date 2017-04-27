from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.Command import Command
from erukar.engine.environment import *
from erukar.engine.model.CoordinateTranslator import CoordinateTranslator
from erukar.engine.model.Direction import Direction
import math

class Map(Command):
    solid_wall = '■'
    door_closed = '□'
    door_open = '-'
    empty_space = ' '
    horiz_door_open = '╶'
    horiz_door_closed = '━'
    vert_door_closed = '┃'
    vert_door_open = '╷'
    player_marker = '@'

    def perform(self, *_):
        '''Converts the dungeon_map into a readable map for the user'''
        return self.fail()
#       player = self.find_player()
#       room = player.character.current_room

#       return self.dimensional_map(player, room)

    def translate_coordinates_to_grid(coords):
        return tuple(map(lambda y: 2*y+1, coords))

    def translate_grid_to_coordinates(grid):
        return tuple(map(lambda y: int((y-1)/2), grid))

    def dimensional_map(self, player, room):
        self.open_space = []
        self.registered_passages = {}
        self.dungeon = room.dungeon
        # Iterate over all of the rooms the player knows about
        #for coord in player.dungeon_map:
        for room in self.dungeon.rooms:
            # Get a list of all coordinates which this room occupies
         #   room = player.dungeon_map[coord]
            self.open_space += list(room.shape.coordinates(room))
            dimensions = (room.width, room.height)
            # Now look at all of the passageways into and out of this room
            for direction in room.connections:
                passage = room.connections[direction]
                # We only care if it's a "door", meaning there's a room behind it
                if passage.is_door():
                    # Translate to the correct coordinates, then find out where the door is supposed to be
                    grid_coords = Map.translate_coordinates_to_grid(room.coordinates)
                    door_coords = CoordinateTranslator.translate_with_dimensions(grid_coords, dimensions, direction)
                    # Make sure we haven't already added it
                    if door_coords not in self.registered_passages:
                        self.registered_passages[door_coords] = passage
        # Now get the min and max range for x and y
        max_x, max_y = map(max, zip(*self.open_space))
        min_x, min_y = map(min, zip(*self.open_space))
        xs = (min_x-1, max_x+2)
        ys = (min_y-1, max_y+2)
        # assume the player is in the center of its current room
        self.player_location = player.lifeform().current_room.center()
        self.append_result(self.sender_uid, '\n'.join(list(self.yield_rows(xs,ys)))[::-1])
        return self.succeed()

    def yield_rows(self, minmax_x, minmax_y):
        for y in range(*minmax_y):
            yield ' '.join([self.decode_location(x,y) for x in range(*minmax_x)][::-1])

    def decode_location(self, x,y):
        '''Determines what character should be drawn at the given coordinate'''
        if (x,y) == self.player_location:
            return Map.player_marker
        if (x,y) in self.open_space:
#           room = self.dungeon.get_room_at(Map.translate_grid_to_coordinates((x,y)))
#           if room is not None:
#               return str(room.linearity)
            return Map.empty_space
        if (x,y) in self.registered_passages:
            return Map.decode_door(self.registered_passages[(x,y)])
        if self.should_draw_as_wall((x,y)):
            return Map.solid_wall
        return ' '

    def should_draw_as_wall(self, coord):
        '''This enforces the off-by-1 rule: only draw IFF next to open space'''
        to_check = []
        for x in range(-1,2):
            for y in range(-1,2):
                to_check.append((coord[0]+x, coord[1]+y))
        return any(actual_room in to_check for actual_room in self.open_space)

    def decode_door(passage):
        '''Draws a door if it exists; then determines if open or closed'''
        if not passage.door:
            return Map.empty_space
        if(passage.door.status is Door.Closed):
            return Map.door_closed
        return Map.door_open
