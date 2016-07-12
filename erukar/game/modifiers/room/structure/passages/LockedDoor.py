from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class LockedDoor(RoomDoorModifier):
    Probability = 0.75
    def __init__(self):
        self.description = "This door is locked."
        self.can_close = True
        self.start_state = Door.Locked
