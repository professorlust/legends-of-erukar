import os, sys
sys.path.append(os.getcwd())

from erukar import *
import erukar

dungeon = Dungeon()

'''Consultants and Dragons'''
# Guild Hall Antechamber (0, 0)
test_room = Room(dungeon, (0,0), dimensions=(2,2), shape=erukar.engine.environment.roomshapes.SouthWestCorner)
a_test_room = Room(dungeon, (2,0), dimensions=(2,2), shape=erukar.engine.environment.roomshapes.SouthEastCorner)
b_test_room = Room(dungeon, (0,2), dimensions=(2,2), shape=erukar.engine.environment.roomshapes.NorthWestCorner)
c_test_room = Room(dungeon, (2,2), dimensions=(2,2), shape=erukar.engine.environment.roomshapes.NorthEastCorner)

test_room.coestablish_connection(Direction.East, a_test_room)
test_room.coestablish_connection(Direction.North, b_test_room)
b_test_room.coestablish_connection(Direction.East, c_test_room)
a_test_room.coestablish_connection(Direction.North, c_test_room)

undead = erukar.game.enemies.undead.Skeleton()
undead.link_to_room(test_room)
undead2 = erukar.game.enemies.undead.Skeleton()
undead2.link_to_room(test_room)


t = Torch()
t.fuel = 100
test_room.add(t)
