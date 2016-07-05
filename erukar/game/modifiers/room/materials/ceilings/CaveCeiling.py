from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class CaveCeiling(RoomModifier):
    Probability = 3

    def apply_to(self, room):
        room.ceiling = Surface('The ceiling is cavernlike. ')
