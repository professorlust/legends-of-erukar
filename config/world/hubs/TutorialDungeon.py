import os, sys
sys.path.append(os.getcwd())

from erukar import *
from erukar.engine.model.Observation import Observation
import erukar

dungeon = Dungeon()
dungeon.name = "Tutorial Dungeon"
dungeon.sovereignty = 'Iuria'
dungeon.region = "Lesser Iurian Razorwoods"
dungeon.description = "An introduction to Legends of Erukar, this dungeon is regularly used by an Adventuring Guild known as \"Consultants and Dragons\" centered in Barlen, Iuria. The dungeon itself is located a half day's journey north from Barlen on the Way of Steel inside of the Lesser Iurian Razorwoods."

# Entry Room
entry = Room(dungeon, (0,0), dimensions = (2,1))
entry.SelfDescription = 'A cold draft wafts through this room. Columns line the northern and southern walls.'
entry.Glances = [
    Observation(acuity=0,  sense=0,  result='The room in this direction is long and narrow.'),
    Observation(acuity=0,  sense=15, result='You hear a soft breeze coming from this room'),
    Observation(acuity=15, sense=0,  result='You see rows of columns on the north and south of this long, narrow room.'),
]

sword = Shop.create(Sword, erukar.game.modifiers.material.Steel)
erukar.game.modifiers.inventory.random.Accurate().apply_to(sword)
erukar.game.modifiers.inventory.random.Freezing().apply_to(sword)
entry.add(sword)

first_room = Room(dungeon, (2,0), dimensions=(2,2), shape=erukar.engine.environment.roomshapes.SouthEastCorner)
first_room.Glances = [
    Observation(acuity = 0, sense=0, result='This room has a sharp ninety degree corner.')
]
first_room.SelfDescription = 'The stone hallway stops abruptly in the direction ahead of you and then quickly shoots off in a ninety degree angle.'

entry.coestablish_connection(Direction.East, first_room)

undead = erukar.game.enemies.undead.Skeleton()
undead.link_to_room(first_room)

t = Torch()
t.fuel = 100
first_room.add(t)
