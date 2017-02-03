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
woodlands_properties = GenerationProfile.Woodlands()

# Entry Room
entry = Room(dungeon, (0,0), dimensions = (2,1))
entry.SelfDescription = 'A cold draft wafts through this room. Columns line the northern and southern walls.'
entry.Glances = [
    Observation(acuity=0,  sense=0,  result='The room in this direction is long and narrow.'),
    Observation(acuity=0,  sense=15, result='You hear a soft breeze coming from this room'),
    Observation(acuity=15, sense=0,  result='You see rows of columns on the north and south of this long, narrow room.'),
]

sword = Shop.create(Sword, erukar.game.modifiers.material.Steel)
erukar.game.modifiers.inventory.random.ScalingAdjustment().apply_to(sword)
entry.add(sword)

'''First Room'''
first_room = Room(dungeon, (2,0), dimensions=(2,2))
first_room.Glances = [
    Observation(acuity = 0, sense=0, result='There is an abnormal chill in the air.')
]
first_room.SelfDescription = 'Your breath visibly mists in front of you -- the air here is terribly brisk'

#entry.coestablish_connection(Direction.East, first_room)

undead = erukar.game.enemies.undead.Skeleton()
undead.link_to_room(first_room)

t = Torch()
t.fuel = 100
first_room.add(t)

'''Second Room'''
second_room = Room(dungeon, (4,0), dimensions=(1,1))
second_room.Glances = [
    Observation(acuity = 0, sense=0, result='There is an abnormal chill in the air.')
]
second_room.SelfDescription = 'Your breath visibly mists in front of you -- the air here is terribly brisk'

first_room.coestablish_connection(Direction.East, second_room)

undead = erukar.game.enemies.undead.Skeleton()
undead.link_to_room(second_room)

dummy_room = Room(dungeon, (5,0), dimensions=(1,1))
entry.coestablish_connection(Direction.East, dummy_room, RandomInstanceTransition('Instance transition door', woodlands_properties))
