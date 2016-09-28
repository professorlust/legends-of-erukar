from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class StoneWalls(RoomModifier):
    ProbabilityFromFabrication = -0.3
    def apply_to(self, room):
        for wall in room.walls():
            wall.BriefDescription = "stone"
            wall.description = "This wall is made of stone"
