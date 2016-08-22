from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class NoLight(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        room.luminosity = random.uniform(0.0, 0.2)
