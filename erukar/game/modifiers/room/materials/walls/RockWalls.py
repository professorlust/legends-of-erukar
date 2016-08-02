from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class RockWalls(RoomModifier):
    ProbabilityFromFabrication = -0.75
    def apply_to(self, room):
        for wall in room.walls():
            wall.description = "This wall is made of rock."
