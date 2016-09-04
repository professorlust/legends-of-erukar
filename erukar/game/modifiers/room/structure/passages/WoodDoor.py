from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class WoodDoor(RoomModifier):
    Probability = 3
    def apply_to(self, room):
        self.description = "There is a wooden door."
        self.can_close = True
        self.start_state = Door.Closed
