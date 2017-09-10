import os, sys
sys.path.append(os.getcwd())

from erukar.system.engine import Npc, TransitionPiece
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

npc = Npc(templates=[erukar.content.Shopkeeper()])
npc.inventory = [
    erukar.content.Halberd(modifiers=[erukar.content.Steel]),
    erukar.content.Burgonet(modifiers=[erukar.content.Leather]),
    erukar.content.Potion()
]
npc.wealth = 100
self.world.add_actor(npc, (1,4))

transition_piece  = TransitionPiece((0,-3,3), (1, -3, 2))
self.world.add_actor(transition_piece, (4,0))