from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class Branch(RoomModifier):
    Probability = 1
    ProbabilityFromFabrication = -0.9

    def apply_to(self, room):
        deco = Decoration(['twigs','twigs and branches','branches'])
        deco.BriefDescription = "twigs and branches on the ground"
        room.add(deco)
