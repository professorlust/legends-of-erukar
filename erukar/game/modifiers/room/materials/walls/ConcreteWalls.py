from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.model.Observation import Observation
import random

class ConcreteWalls(RoomModifier):
    ProbabilityFromFabrication = 0.6

    textures = [
        "smooth",
        "coarse",
        "polished"
    ]

    def __init__(self):
        self.texture = random.choice(self.textures)
        super().__init__()

    Glances = [
        Observation(acuity=0, sense=0, result="made of concrete"),
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="This wall is made of concrete"),
        Observation(acuity=10, sense=0, result="This wall is made of {texture} concrete"),
    ]

    def apply_to(self, room):
        for wall in room.walls():
            wall.Glances = wall.Glances + self.Glances
            wall.Inspects = wall.Inspects + self.Inspects
