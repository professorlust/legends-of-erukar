import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import TransitionPiece, Dungeon, Room, Wall, TileGenerator, Door
from erukar.ext.math import Shapes
import erukar

dungeon = Dungeon()
antechamber = Room(dungeon, coordinates=Shapes.rect((0, 8), (0, 16)))

# add columns
columns = []
for y in range(2, 16, 4):
    columns += [(2, y), (6, y)]

dungeon.remove_space(columns)
closed_space = list(Shapes.rect((-1,9),(-1,17)))

dungeon.apply_tiles_on_all_open_space(erukar.content.StoneFloor())
dungeon.apply_tiles_on_closed_space(closed_space, erukar.content.StoneBricks())
dungeon.apply_tiles_on_closed_space(columns, erukar.content.StoneWall())

dungeon.spawn_coordinates = [(1,1)]
transition_piece = TransitionPiece("IzethCitadel1F", (0,-2,2))
dungeon.add_transition(transition_piece, (1,1))

dungeon.generate_tiles(TileGenerator(dungeon))
