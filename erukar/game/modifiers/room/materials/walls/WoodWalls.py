from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class WoodWalls(RoomModifier):
    ProbabilityFromFabrication = 0.1
    def apply_to(self, room):
        for wall in room.walls():
            wall.BriefDescription = "wooden"
            wall.description = "This wall is made of wood."
