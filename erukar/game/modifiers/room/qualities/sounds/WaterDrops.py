from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class WaterDrops(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        deco = Decoration(aliases=['water droplets', 'drops of water', 'droplets of water'])
        room.add(deco)
