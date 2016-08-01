from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class GalvanizedSteelFloor(RoomModifier):
    ProbabilityFromFabrication = 1.0

    def apply_to(self, room):
        room.floor = Surface('The floor seems to be made of a galvanized steel with tread patterns.')
