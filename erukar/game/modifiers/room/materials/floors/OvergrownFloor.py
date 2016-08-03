from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class OvergrownFloor(RoomModifier):
    Proability = 1.1
    ProbabilityFromFabrication = -0.8

    def apply_to(self, room):
        room.floor = Surface('You cannot see the floor through the dense overgrowth.')

