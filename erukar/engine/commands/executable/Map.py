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
#        return self.complex_map(player, room)

#--------------------------------------------------------------------------
    def translate_coordinates_to_grid(coords):
        return tuple(map(lambda y: 2*y+1, coords))
#--------------------------------------------------------------------------

    def dimensional_map(self, player, room):
        occupied_coords = []
        registered_passages = {}
        for coord in player.dungeon_map:
            room = player.dungeon_map[coord]
            occupied_coords += list(Map.room_coordinates(room))
            for direction in room.connections:
                passage = room.connections[direction]
                if passage.is_door():
                    door_coords = CoordinateTranslator.translate(Map.translate_coordinates_to_grid(room.coordinates), direction)
                    if door_coords not in registered_passages:
                        registered_passages[door_coords] = passage
        max_x, max_y = map(max, zip(*occupied_coords))
        min_x, min_y = map(min, zip(*occupied_coords))
        xs = (min_x-1, max_x+2)
        ys = (min_y-1, max_y+2)
        player_loc = Map.translate_coordinates_to_grid(player.lifeform().current_room.coordinates)
        print('\n'.join(list(self.yield_rows(xs,ys, player_loc, occupied_coords, registered_passages)))[::-1])

    def yield_rows(self, minmax_x, minmax_y, player_loc, all_coordinates_occupied, passages):
        for y in range(*minmax_y):
            yield ' '.join([Map.decode_location(x,y,player_loc,all_coordinates_occupied,passages) for x in range(*minmax_x)][::-1])

    def decode_location(x,y, player_loc, all_coordinates_occupied, passages):
        if (x,y) == player_loc:
            return Map.player_marker
        if (x,y) in passages:
            return Map.decode_door(passages[(x,y)])
        if (x,y) in all_coordinates_occupied:
            return Map.empty_space
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

    def room_coordinates(room):
        x_i, y_i = Map.translate_coordinates_to_grid(room.coordinates)
        for x in range(2*room.width-1):
            for y in range(2*room.height-1):
                yield (x_i+x, y_i+y)

    def complex_map(self, player, room):
        '''Draw a MASSIVE map where each coordinate is a 3x3; draws doors, too'''
        max_x, max_y = map(max, zip(*player.dungeon_map))
        min_x, min_y = map(min, zip(*player.dungeon_map))
        drawn_doors = set()

        # First pass: Find the rooms and make the blocks around them
        dnjn_map = [[self.complex_map_location(x, y, player.dungeon_map)
            for x in range(3*(min_x), 3*(max_x+1))] for y in range(3*(min_y), 3*(max_y+1))]

        # Second pass: Add the doors where appropriate
        for r in player.dungeon_map:
            self.complex_add_doors(dnjn_map, player.dungeon_map[r], min_x, min_y, drawn_doors)

        # show the player as an X
        self.complex_add_player(room.coordinates, dnjn_map, min_x, min_y)
        self.append_result(self.sender_uid, '\n'.join(' '.join(y) for y in reversed(dnjn_map)))
        return self.succeed()

    def complex_map_location(self, x, y, dungeon_map):
        '''Add a cell to the complex map; only concerned with walls!'''
        if ((x-1)/3, (y-1)/3) in dungeon_map:
            return Map.empty_space
        if (math.floor((x)/3), math.floor((y)/3)) in dungeon_map:
            return Map.solid_wall
        return Map.empty_space

    def complex_add_player(self, player_coordinates, dungeon_map, min_x, min_y):
        '''Add a player indicator to the complex map'''
        x, y = ((player_coordinates[0]-min_x)*3+1, (player_coordinates[1]-min_y)*3+1)
        dungeon_map[y][x] = Map.player_marker

    def complex_add_doors(self, dungeon_map, room, min_x, min_y, drawn_doors):
        '''Draws the doors and passageways in a complex map'''
        lifeform = self.find_player().lifeform()
        x, y = room.coordinates
        center_x, center_y = ((x-min_x)*3+1, (y-min_y)*3+1)

        for connection in room.connections:
            if room.connections[connection].can_see_or_sense(lifeform):
                dy, dx = CoordinateTranslator.translate((center_x, center_y), connection)
                dungeon_map[dx][dy] = self.passage_to_icon(room.connections[connection], connection, drawn_doors)

    def passage_to_icon(self, connection, direction, drawn_doors):
        '''Converts a passage type to its appropriate icon'''
        if connection.door is not None and connection.door not in drawn_doors:
            drawn_doors.add(connection.door)
            if isinstance(connection.door, Door) and connection.door.can_close:
                if direction is Direction.North or direction is Direction.South:
                    return Map.horiz_door_open if connection.door.status is Door.Open else Map.horiz_door_closed
                return Map.vert_door_open if connection.door.status is Door.Open else Map.vert_door_closed

        if connection.room is not None:
            return Map.empty_space
        return Map.solid_wall
