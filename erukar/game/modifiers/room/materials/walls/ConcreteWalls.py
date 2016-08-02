from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class ConcreteWalls(RoomModifier):
    ProbabilityFromFabrication = 0.6
    textures = [
        "smooth",
        "coarse",
        "polished"
    ]

    def __init__(self):
        super().__init__()
        self.texture = random.choice(self.textures)
        self.description = "This wall is made of a {} concrete.".format(self.texture)

    def apply_to(self, room):
        for wall in room.walls():
            wall.description = self.description 
