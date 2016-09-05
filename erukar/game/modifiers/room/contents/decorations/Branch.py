from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class Branch(RoomModifier):
    Probability = 1
    ProbabilityFromFabrication = -0.9

    def apply_to(self, room):
        deco = Decoration(['a branch'])
        deco.set_vision_results('There are twigs and branches on the ground.', 'Strewn throughout the ground is an assortment of twigs and branches.', (1, 4))
        deco.set_sensory_results('You smell freshly cut wood.', 'You smell twigs, branches, and other broken pieces of wood.', (5, 10))
        deco.set_detailed_results('There are twigs and branchs on the ground.', 'Strewn throughout the ground is an assortment of twigs and branches.')
        room.add(deco)
