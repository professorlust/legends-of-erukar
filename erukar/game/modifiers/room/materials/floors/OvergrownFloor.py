from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class OvergrownFloor(RoomModifier):
    Proability = 1.1
    ProbabilityFromFabrication = -0.8

    def apply_to(self, room):
        room.floor = Surface('You can hardly see the dirt and grass in some areas of this area due to the heavy overgrowth.')

