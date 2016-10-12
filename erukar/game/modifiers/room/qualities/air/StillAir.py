from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class StillAir(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        pass
#       room.sense_minimal += ' The room feels unsettling and stagnant.'
#       room.sense_ideal += ' There is no air current circulating in the room.'
