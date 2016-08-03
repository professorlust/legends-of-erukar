from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class RockyFloor(RoomModifier):
    Proability = 2.0
    ProbabilityFromFabrication = -0.5

    def apply_to(self, room):
        room.floor = Surface('The floor below you is covered in broken rocks and gravel.')
