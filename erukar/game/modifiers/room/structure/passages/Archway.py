from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class Archway(RoomDoorModifier):
    ProbabilityFromFabrication = 1.0
    description = "An archway opens into another room."
    can_close = False
    start_state = Door.Open
