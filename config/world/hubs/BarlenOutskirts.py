import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import Npc, TransitionPiece, Dungeon, Room, Wall, TileGenerator
import erukar

dungeon = Dungeon()

area = []
for x in range(5):
    for y in range(5):
        area += [(x,y)]

north_area = Room(dungeon, coordinates=area)

path = [
    (4,0),(4,1),(1,10),(2,10)
]
path += [(3,y) for y in range(1,11)]
path += [(x,5) for x in range(4,9)]

'''Add Walls'''
pine_tex =  erukar.content.Pine()
xo, yo = map(min, zip(*dungeon.dungeon_map))
xf, yf = map(max, zip(*dungeon.dungeon_map))
for y in range(yo-1, yf+2):
    for x in range(xo-1, xf+2):
        if (x,y) not in dungeon.dungeon_map:
            wall = Wall()
            wall.material = pine_tex
            dungeon.walls[(x, y)] = wall
            dungeon.tiles[(x, y)] = pine_tex

'''decorate ground'''
grass_tex = erukar.content.Grass()
dirt_tex = erukar.content.Dirt()
for loc in dungeon.all_traversable_coordinates():
    dungeon.tiles[loc] = dirt_tex if loc in path else grass_tex

dungeon.generate_tiles(TileGenerator(dungeon))

dungeon.spawn_coordinates = [(1,1)]

transition_piece  = TransitionPiece((0,0,0), (0, -1, 1))
dungeon.add_actor(transition_piece, (1,1))
