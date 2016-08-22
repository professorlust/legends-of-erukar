from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class BrightLight(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        room.luminosity = random.uniform(0.8, 1.0)
