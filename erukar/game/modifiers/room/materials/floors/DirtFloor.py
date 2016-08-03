from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class DirtFloor(RoomModifier):
    Proability = 2.0
    ProbabilityFromFabrication = -0.8

    def apply_to(self, room):
        room.floor = Surface('The flooring of this room is packed dirt. ')
