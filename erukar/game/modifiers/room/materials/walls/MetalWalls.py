from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class MetalWalls(RoomModifier):
    ProbabilityFromFabrication = 1.0
    def apply_to(self, room):
        for wall in room.walls():
            wall.BriefDescription = "metal"
            wall.description = "This wall is made of metal."
