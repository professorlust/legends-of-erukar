from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door, Key, EnchantedLock
import random

class MagicLockedDoor(RoomDoorModifier):
    Probability = 5
    ProbabilityFromFabrication = 0.75

    def __init__(self):
        self.description = 'You see {describe_locked} door to the {direction}. The door is {status}. {describe_lock}'
        self.can_close = True
        self.start_state = Door.Closed
        self.lock = EnchantedLock('abra cadabra')
        self.lock.description = 'On the door are several faint, glowing runes.'
