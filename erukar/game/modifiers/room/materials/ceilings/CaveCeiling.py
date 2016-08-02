from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class CaveCeiling(RoomModifier):
    ProbabilityFromFabrication = -0.5
    ProbabilityFromAltitude = -0.5

    def apply_to(self, room):
        room.ceiling = Surface('The ceiling is cavernlike. ')
