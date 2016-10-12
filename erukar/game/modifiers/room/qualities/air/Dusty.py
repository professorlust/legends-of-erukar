from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class Dusty(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        pass
#        room.sense_minimal += ' The air is dusty.'
#        room.sense_ideal += ' A thick layer of dust covers nearly everything in the room.'
