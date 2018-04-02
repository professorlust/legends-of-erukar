import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import Npc, TransitionPiece, Dungeon, Room, Wall, TileGenerator, Door
from erukar.ext.math import Shapes
import erukar

dungeon = Dungeon()

w_area = list(Shapes.rect((0,5), (0,7)))
west_area = Room(dungeon, coordinates=w_area)

'''Add Preliminary Pine Walls'''
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
    dungeon.tiles[loc] = grass_tex

'''decorate building'''
def create_shop_building():
    area = list(Shapes.rect((-6,-2), (2,5)))
    area += [(-1,3)]
    Room(dungeon, coordinates=area)
    wall = erukar.content.StoneBricks()
    floor = erukar.content.StoneFloor()
    '''Add Walls first to avoid conflict at door'''
    min_x, min_y = min(area)
    max_x, max_y = max(area)
    for x in range(-7, -1):
        dungeon.tiles[(x, 1)] = wall
        dungeon.tiles[(x, 6)] = wall
    for y in range(1, 6):
        dungeon.tiles[(-6, y)] = wall
        dungeon.tiles[(-1, y)] = wall
    '''Then add floors'''
    for loc in area:
        dungeon.tiles[loc] = floor

create_shop_building()

dungeon.generate_tiles(TileGenerator(dungeon))
dungeon.spawn_coordinates = [(1,1)]

transition_piece  = TransitionPiece((0,0,0), (0, -1, 1))
dungeon.add_transition(transition_piece, (1,5))
dungeon.add_door(Door(), (-1,3))

npc = Npc(templates=[erukar.content.Shopkeeper()])
npc.name = erukar.ext.math.Namer.random()
npc.inventory = [
    erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
    erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
    erukar.content.Axe(modifiers=[erukar.content.Iurwood]),
    erukar.content.Club(modifiers=[erukar.content.Oak]),
    erukar.content.Dagger(modifiers=[erukar.content.Iron]),
    erukar.content.Dagger(modifiers=[erukar.content.Iron]),
    erukar.content.Dagger(modifiers=[erukar.content.Steel]),
    erukar.content.Dagger(modifiers=[erukar.content.Steel]),
    erukar.content.Longsword(modifiers=[erukar.content.Iron]),
    erukar.content.Longsword(modifiers=[erukar.content.Steel]),
    erukar.content.Longsword(modifiers=[erukar.content.Steel]),
    erukar.content.Mace(modifiers=[erukar.content.Iron]),
    erukar.content.Mace(modifiers=[erukar.content.Iron]),
    erukar.content.Shortbow(modifiers=[erukar.content.Iurwood]),
    erukar.content.Shortbow(modifiers=[erukar.content.Oak]),
    erukar.content.Shortbow(modifiers=[erukar.content.Oak]),
    erukar.content.Guard(modifiers=[erukar.content.Leather]),
    erukar.content.Guard(modifiers=[erukar.content.Leather]),
    erukar.content.Robes(modifiers=[erukar.content.Cotton]),
    erukar.content.Robes(modifiers=[erukar.content.Cotton]),
    erukar.content.Vest(modifiers=[erukar.content.Leather]),
    erukar.content.Vest(modifiers=[erukar.content.Leather]),
    erukar.content.Boots(modifiers=[erukar.content.Leather]),
    erukar.content.Boots(modifiers=[erukar.content.Leather]),
    erukar.content.Treads(modifiers=[erukar.content.Leather]),
    erukar.content.Treads(modifiers=[erukar.content.Leather]),
    erukar.content.Gloves(modifiers=[erukar.content.Leather]),
    erukar.content.Gloves(modifiers=[erukar.content.Leather]),
    erukar.content.Cap(modifiers=[erukar.content.Cotton]),
    erukar.content.Cap(modifiers=[erukar.content.Cotton]),
    erukar.content.Barbute(modifiers=[erukar.content.Iron]),
    erukar.content.Barbute(modifiers=[erukar.content.Iron]),
    erukar.content.Leggings(modifiers=[erukar.content.Chainmail]),
    erukar.content.Leggings(modifiers=[erukar.content.Chainmail]),
    erukar.content.Breeches(modifiers=[erukar.content.Leather]),
    erukar.content.Breeches(modifiers=[erukar.content.Leather]),
    erukar.content.Breeches(modifiers=[erukar.content.Cotton]),
    erukar.content.Buckler(modifiers=[erukar.content.Iron]),
    erukar.content.Buckler(modifiers=[erukar.content.Iron]),
    erukar.content.HeaterShield(modifiers=[erukar.content.Steel]),
    erukar.content.HeaterShield(modifiers=[erukar.content.Steel]),
    erukar.content.Potion(25),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Torch(),
    erukar.content.Arrow(50, modifiers=[erukar.content.Atherite]),
    erukar.content.CrossbowBolt(50, modifiers=[erukar.content.Salericite]),
]
npc.wealth = 1500
dungeon.add_actor(npc, (-4,2))
