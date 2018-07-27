from erukar.system.engine import Npc, TransitionPiece, OverlandZone, Room, Wall, TileGenerator, Door
from erukar.ext.math import Shapes
import erukar
import sys
import os
sys.path.append(os.getcwd())

dungeon = OverlandZone()
wall_texture = erukar.content.StoneBricks()
floor_texture = erukar.content.WoodFloor()

''' Path into Town '''
path_into_town = Room(dungeon, coordinates=Shapes.rect((0, 10), (0, 2)))
dungeon.apply_tiles_to_room(path_into_town, open_tile=erukar.content.Grass())

''' Arcanist Shop '''
arcanist_shop = Room(dungeon, coordinates=Shapes.rect((1,3),(4,6)))
arcanist_shop.annex([(2, 3)])
dungeon.apply_tiles_to_room(arcanist_shop, open_tile=floor_texture)
alchemist = Npc(templates=[erukar.content.Alchemist])
dungeon.add_npc(alchemist, arcanist_shop)
alchemist.use_standard_inventory()
alchemist.wealth = 800
dungeon.add_actor(erukar.content.Torch(), (2,5))
dungeon.add_door(Door(), (2, 3))

''' Trade Commissioner '''
trade_commission = Room(dungeon, coordinates=Shapes.rect((7,9),(4,6)))
trade_commission.annex([(8, 3)])
dungeon.apply_tiles_to_room(trade_commission, open_tile=floor_texture)
commissioner = Npc(templates=[erukar.content.TradeCommissioner])
dungeon.add_npc(commissioner, trade_commission)
commissioner.use_standard_inventory()
commissioner.wealth = 1500
dungeon.add_door(Door(), (8, 3))

''' Smithy '''
smithy = Room(dungeon, coordinates=Shapes.rect((1,3),(-4,-2)))
smithy.annex([(2, -1)])
dungeon.apply_tiles_to_room(smithy, open_tile=erukar.content.StoneFloor())
smith_npc = Npc(templates=[erukar.content.Smithy])
dungeon.add_npc(smith_npc, smithy)
smith_npc.use_standard_inventory()
smith_npc.wealth = 500
dungeon.add_door(Door(), (2, -1))

''' Wall Textures '''
dungeon.apply_tiles_on_all_closed_space(erukar.content.Pine())
dungeon.apply_tiles_on_closed_space(Shapes.rect((0,4), (3,7)), wall_texture)
dungeon.apply_tiles_on_closed_space(Shapes.rect((0,4), (-5,-1)), wall_texture)
dungeon.apply_tiles_on_closed_space(Shapes.rect((6,10),(3,7)), wall_texture)

''' Establish Spawn Location and generate Tiles'''
dungeon.generate_tiles(TileGenerator(dungeon))
dungeon.spawn_coordinates = [(10,1)]
transition_piece = TransitionPiece((0, 0), (1, 0))
dungeon.add_transition(transition_piece, (10,1))


''' Sheriff '''
sheriff = Npc(
    templates=[erukar.Conversationalist],
    conversation='BarlenSheriff'
)
dungeon.add_npc(sheriff, trade_commission)
