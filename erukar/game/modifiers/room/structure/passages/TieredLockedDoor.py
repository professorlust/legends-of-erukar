from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door, Key, TieredLock
import random

class TieredLockedDoor(RoomDoorModifier):
    Probability = 1
    ProbabilityFromFabrication = 0.75

    def __init__(self):
        self.description = 'You see {describe_locked} door to the {direction}. The door is {status}.'
        self.can_close = True
        self.start_state = Door.Closed
        self.lock = TieredLock(1.0)
