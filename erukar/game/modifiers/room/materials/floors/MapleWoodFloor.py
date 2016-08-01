from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface

class MapleWoodFloor(RoomModifier):
    ProbabilityFromFabrication = 0.1

    def apply_to(self, room):
        room.floor = Surface('The floor is made of maple hardwood.')
