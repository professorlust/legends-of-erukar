from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class Archway(RoomDoorModifier):
    ProbabilityFromFabrication = 1.0
    description = "An archway to the {0} opens into another room."
    can_close = False
    start_state = Door.Open
