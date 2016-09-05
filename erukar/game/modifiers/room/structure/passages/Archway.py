from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class Archway(RoomDoorModifier):
    ProbabilityFromFabrication = 1.0
    description = "An archway in this area opens up to the {direction}."
    can_close = False
    start_state = Door.Open
