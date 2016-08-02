from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class WoodCeiling(RoomModifier):
    ProbabilityFromFabrication = 0.8

    def apply_to(self, room):
        room.ceiling = Surface('The ceiling is made of wood. ')
