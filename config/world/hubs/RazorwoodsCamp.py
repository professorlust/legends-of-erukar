import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import Npc, TransitionPiece, Dungeon, Room, Wall, TileGenerator
import erukar

dungeon = Dungeon()
coords = [(4,0),(3,1), (4,1),(2,2), (3,2), (4,2),(2,3), (3,3), (4,3), (5,3), (6,3),(1,4), (2,4), (3,4), (5,4), (5,5),(1,5), (2,5), (3,5), (4,5), (5,5), (6,5),(2,6), (3,6), (4,6), (5,6), (6,6),(2,7), (3,7), (4,7),(2,8), (3,8), (9,8), (10,8), (11,8), (7,9), (8,9), (9,9), (10,9), (11,9), (7,10), (8,10), (9,10), (10,10), (11,10), (12,10),(9,11), (10,11), (11,11),(10,12), (11,12),(10,12), (1,9), (2,9), (3,9), (4,9),(1,10), (2,10), (3,10), (4,10), (5,10), (6,10),(2,11), (3,11), (4,11), (5,11),(4,12), (5,12), (6,12), (9,3), (10,3),(7,4), (8,4), (9,4), (10,4), (11,4),(7,5), (8,5), (9,5), (10,5),(7,6), (8,6), (9,6),(7,7), (8,7), (9,7), (10,7), (11,7)]

area = Room(dungeon, coordinates=coords)
path = [(4,0),(4,1),(1,10),(2,10)] + [(3,y) for y in range(1,11)] + [(x,5) for x in range(4,9)]

'''Set basic tiles'''
dungeon.apply_tiles_on_all_closed_space(erukar.content.Pine())
dungeon.apply_tiles_on_all_open_space(erukar.content.Grass())
dungeon.apply_tiles_on_open_space(path, erukar.content.Dirt())
dungeon.generate_tiles(TileGenerator(dungeon))

'''Spawn Point'''
transition_piece  = TransitionPiece((0,-3,3), (1, -3, 2))
dungeon.add_transition(transition_piece, (4,0))
dungeon.spawn_coordinates = [(4,0)]

'''Forester'''
forester = Npc(templates=[erukar.content.Forester])
dungeon.add_npc(forester, (1,4))
forester.use_standard_inventory()
forester.wealth = 50

'''Fletcher'''
fletcher = Npc(templates=[erukar.content.Fletcher])
dungeon.add_npc(fletcher, (4,5))
fletcher.use_standard_inventory()
fletcher.wealth = 70
