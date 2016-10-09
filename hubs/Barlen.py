import os, sys
sys.path.append(os.getcwd())

from erukar import *

dungeon = Dungeon()
r1 = Room(dungeon, (0,0))
r1.SelfDescription = 'This room is ornately built.'
r2 = Room(dungeon, (0,1))
r2.SelfDescription = 'This is the Kingspath Street.'
r1.coestablish_connection(Direction.North, r2)
