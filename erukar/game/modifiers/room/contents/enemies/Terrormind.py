from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import erukar

class Terrormind(RoomModifier):
    Probability = 0.05
    def apply_to(self, room):
        terrormind = erukar.game.enemies.Terrormind()
#        print(terrormind)
        terrormind.define_level(4)
        terrormind.current_room = room
        room.add(terrormind)
