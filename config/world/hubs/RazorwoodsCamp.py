import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import Npc, TransitionPiece, Dungeon, Room, Wall, TileGenerator
import erukar

dungeon = Dungeon()

north_area = Room(dungeon, coordinates=[
    (4,0),
    (3,1), (4,1),
    (2,2), (3,2), (4,2),
    (2,3), (3,3), (4,3), (5,3), (6,3),
    (1,4), (2,4), (3,4), (5,4), (5,5),
    (1,5), (2,5), (3,5), (4,5), (5,5), (6,5),
    (2,6), (3,6), (4,6), (5,6), (6,6),
    (2,7), (3,7), (4,7),
    (2,8), (3,8)
])

south_area = Room(dungeon, coordinates=[
    (1,9), (2,9), (3,9), (4,9),
    (1,10), (2,10), (3,10), (4,10), (5,10), (6,10),
    (2,11), (3,11), (4,11), (5,11),
    (4,12), (5,12), (6,12)
])

northeast_area = Room(dungeon, coordinates=[
    (9,3), (10,3),
    (7,4), (8,4), (9,4), (10,4), (11,4),
    (7,5), (8,5), (9,5), (10,5),
    (7,6), (8,6), (9,6),
    (7,7), (8,7), (9,7), (10,7), (11,7),
])

southeast_area = Room(dungeon, coordinates=[
    (9,8), (10,8), (11,8),
    (7,9), (8,9), (9,9), (10,9), (11,9),
    (7,10), (8,10), (9,10), (10,10), (11,10), (12,10),
    (9,11), (10,11), (11,11),
    (10,12), (11,12),
    (10,12)
])

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

dungeon.generate_tiles(TileGenerator(dungeon.pixels_per_side, dungeon.pixels_per_side))


dungeon.spawn_coordinates = [(4,0)]

npc = Npc(templates=[erukar.content.Shopkeeper()])
npc.name = erukar.ext.math.Namer.random()
npc.inventory = [
    erukar.content.Potion(10),
    erukar.content.Candle(),
    erukar.content.Candle(),
    erukar.content.Candle(),
    erukar.content.Candle(),
    erukar.content.Candle(),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Arrow(50),

]
npc.wealth = 1000
dungeon.add_actor(npc, (1,4))

transition_piece  = TransitionPiece((0,-3,3), (1, -3, 2))
dungeon.add_actor(transition_piece, (4,0))
