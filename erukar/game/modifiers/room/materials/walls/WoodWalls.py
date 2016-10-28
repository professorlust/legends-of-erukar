from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.model.Observation import Observation

class WoodWalls(RoomModifier):
    ProbabilityFromFabrication = 0.1

    Glances = [
        Observation(acuity=0, sense=0, result="made of wood"),
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="This wall is made of wood.")
    ]

    def apply_to(self, room):
        for wall in room.walls():
            wall.Glances = wall.Glances + self.Glances
            wall.Inspects = wall.Inspects + self.Inspects
