from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class Archway(RoomDoorModifier):
    ProbabilityFromFabrication = 1.0

    def __init__(self):
        self.description = "An archway to the {0} opens into another room."
        self.can_close = False
        self.start_state = Door.Open
