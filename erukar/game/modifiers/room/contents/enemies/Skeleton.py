from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import erukar

class Skeleton(RoomModifier):
    Probability = 20
    def apply_to(self, room):
        skelly = erukar.game.enemies.Skeleton()
#        print(skelly)
        skelly.define_level(1)
        skelly.current_room = room
        room.add(skelly)
