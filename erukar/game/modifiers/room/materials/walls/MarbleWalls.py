from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class MarbleWalls(RoomModifier):
    ProbabilityFromFabrication = 0.75
    def apply_to(self, room):
        for wall in room.walls():
            wall.BriefDescription = "marble"
            wall.description = "This wall is made of marble."
