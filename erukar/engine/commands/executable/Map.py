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

    aliases = ['map']

    def execute(self, *_):
        '''Converts the dungeon_map into a readable map for the user'''
        player = self.find_player()
        room = player.character.current_room

        return self.dimensional_map(player, room)

    def translate_coordinates_to_grid(coords):
        return tuple(map(lambda y: 2*y+1, coords))

    def dimensional_map(self, player, room):
        occupied_coords = []
        registered_passages = {}
        for coord in player.dungeon_map:
            room = player.dungeon_map[coord]
            occupied_coords += list(room.shape.coordinates(room))
            dimensions = (room.width, room.height)
            for direction in room.connections:
                passage = room.connections[direction]
                if passage.is_door():
                    grid_coords = Map.translate_coordinates_to_grid(room.coordinates)
                    door_coords = CoordinateTranslator.translate_with_dimensions(grid_coords, dimensions, direction)
                    if door_coords not in registered_passages:
                        registered_passages[door_coords] = passage
        max_x, max_y = map(max, zip(*occupied_coords))
        min_x, min_y = map(min, zip(*occupied_coords))
        xs = (min_x-1, max_x+2)
        ys = (min_y-1, max_y+2)
        player_loc = player.lifeform().current_room.center()
        print('\n'.join(list(self.yield_rows(xs,ys, player_loc, occupied_coords, registered_passages)))[::-1])

    def yield_rows(self, minmax_x, minmax_y, player_loc, all_coordinates_occupied, passages):
        for y in range(*minmax_y):
            yield ' '.join([Map.decode_location(x,y,player_loc,all_coordinates_occupied,passages) for x in range(*minmax_x)][::-1])

    def decode_location(x,y, player_loc, all_coordinates_occupied, passages):
        if (x,y) == player_loc:
            return Map.player_marker
        if (x,y) in all_coordinates_occupied:
            return Map.empty_space
        if (x,y) in passages:
            return Map.decode_door(passages[(x,y)])
        if Map.should_draw_as_wall((x,y), all_coordinates_occupied, passages):
            return Map.solid_wall
        return ' '

    def should_draw_as_wall(coord, occupied_coords, passages):
        to_check = []
        for x in range(-1,2):
            for y in range(-1,2):
                to_check.append((coord[0]+x, coord[1]+y))
        return any(actual_room in to_check for actual_room in occupied_coords)

    def decode_door(passage):
        if not passage.door:
            return Map.empty_space
        if(passage.door.status is Door.Closed):
            return Map.door_closed
        return Map.door_open
