from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class NoItem(RoomModifier):
    Probability = 2.0
    def apply_to(self, room):
        pass
