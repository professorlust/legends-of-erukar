from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class NoDecoration(RoomModifier):
    Probability = 10
    def apply_to(self, room):
        pass
