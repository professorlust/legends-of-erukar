from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class TiledFloor(RoomModifier):
    ProbabilityFromFabrication = 0.6

    def apply_to(self, room):
        room.floor = Surface('The floor is made of ceramic tiles arranged in a checker pattern.')
