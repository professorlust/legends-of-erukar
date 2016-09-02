from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
import random

class Stove(RoomModifier):
    Probability = 0.00
    ProbabilityFromFabrication = 1.0

    broad_alias_base = 'stove'
    broad_result_base = 'There is a stove {} of the room.'
    inspect_result_base = 'This is a well-used stove. It is currently cold and does not appear to have been used recently.'

    def apply_to(self, room):
        try:
            location = 'to the ' + random.choice(list(room.wall_directions())).name
        except:
            location = 'in the center'
        deco = Decoration(aliases=[self.broad_alias_base],\
            broad_results=self.broad_result_base.format(location),\
            inspect_results=self.inspect_result_base)
        room.add(deco)
