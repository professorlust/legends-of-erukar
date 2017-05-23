import os, sys
sys.path.append(os.getcwd())

from erukar import *
from erukar.engine.model.Observation import Observation
from erukar.game.modifiers import *
import erukar

dungeon = Dungeon()
dungeon.name = "Tutorial Dungeon"
dungeon.sovereignty = 'Iuria'
dungeon.region = "Lesser Iurian Razorwoods"
dungeon.description = "An introduction to Legends of Erukar, this dungeon is regularly used by an Adventuring Guild known as \"Consultants and Dragons\" centered in Barlen, Iuria. The dungeon itself is located a half day's journey north from Barlen on the Way of Steel inside of the Lesser Iurian Razorwoods."
woodlands_properties = GenerationProfile.Woodlands()

# Entry Room
entry = Room(dungeon, coordinates=[(0,0), (1,0), (2,0)])
entry.SelfDescription = 'A cold draft wafts through this room. Columns line the northern and southern walls.'
entry.Glances = [
    Observation(acuity=0,  sense=0,  result='The room in this direction is long and narrow.'),
    Observation(acuity=0,  sense=15, result='You hear a soft breeze coming from this room'),
    Observation(acuity=15, sense=0,  result='You see rows of columns on the north and south of this long, narrow room.'),
]

sword = Sword(modifiers=[modifiers.Salericite, modifiers.Quality, modifiers.Size, modifiers.Bane])
dungeon.add_actor(sword, (0,1))

arrow = Arrow(modifiers=[modifiers.Steel])
dungeon.add_actor(arrow, (0,1))

bow = Shop.create(Bow, erukar.game.modifiers.material.Oak)
erukar.game.modifiers.inventory.universal.Quality().apply_to(bow)
dungeon.add_actor(bow, (0,2))

second_room = Room(dungeon, coordinates=[(x,y) for x in range(3,5) for y in range(-1,2)])

sk = Skeleton()
dungeon.add_actor(sk, (3, -1))

third_room = Room(dungeon, coordinates=[(5,1)] + [(6,1+x) for x in range(0,5)])
fourth_room = Room(dungeon, coordinates=[(x,y) for x in range(2,6) for y in range(4,6)])
