from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import erukar

class Skeleton(RoomModifier):
    Probability = 10
    def apply_to(self, room):
        skelly = erukar.game.enemies.undead.Skeleton()
        skelly.current_room = room
        room.add(skelly)
