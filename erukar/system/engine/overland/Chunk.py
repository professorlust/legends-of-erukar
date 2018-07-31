from erukar.system.engine import Room, Door, TransitionPiece
from erukar.ext.math import Shapes
import erukar


class Chunk:
    def generate(self, vertex, dungeon):
        x, y = vertex
        # create spaces
        outdoor_space = list(Shapes.rect( (x-2,x+4), (y-2,y+4) ))
        closed_space = list(Shapes.rect( (x-1,x+3), (y-1,y+3) ))
        indoor_space = list(Shapes.rect( (x, x+2), (y, y+2)))
        indoor_space.append((x+1, y+3))

        dungeon.remove_space(outdoor_space)
        outdoor_space = [p for p in outdoor_space if p not in closed_space]

        Room(dungeon, coordinates=outdoor_space)
        Room(dungeon, coordinates=indoor_space)
        outdoor_floor_tile = erukar.content.Grass()
        indoor_floor_tile = erukar.content.StoneFloor()
        wall_tile = erukar.content.StoneBricks()
        dungeon.apply_tiles_on_closed_space(closed_space, wall_tile)
        dungeon.apply_tiles_on_open_space(outdoor_space, outdoor_floor_tile)
        dungeon.apply_tiles_on_open_space(indoor_space, indoor_floor_tile)

        door = Door()
        door.lock_type = erukar.Silver
        key = erukar.Key(modifiers=[erukar.Silver])
        dungeon.add_actor(key, (x+1, y+4))

        dungeon.add_door(door, (x+1, y+3))
        to_izeth  = TransitionPiece((0, -2, 2), "IcamoreCrypts1F")
        dungeon.add_transition(to_izeth, (x, y))
