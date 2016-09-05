from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class Hallway(RoomModifier):
    description = 'The {direction} opens up into a hallway without a door.'
    ProbabilityFromFabrication = 1
