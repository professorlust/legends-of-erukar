from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class ClayCeiling(RoomModifier):
    ProbabilityFromFabrication = 0.4

    def apply_to(self, room):
        room.ceiling = Surface('The ceiling is made of clay. ')
