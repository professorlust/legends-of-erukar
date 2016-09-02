from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random

class Altar(RoomModifier):
    Probability = 0
    ProbabilityFromFabrication = 0.1
    ProbabilityFromSanctity = 1.0

    broad_alias_base = 'altar'
    broad_result_base = 'An altar sits to the {} of the room'
    inspect_results_base = 'This is an altar to {}. '

    deity_possibilities = [
        'the God Omanis',
        'the Goddess Crepascia',
        'the God Olevarde',
        'Lord Ravodin, Protector of the Light']

    def apply_to(self, room):
        deity = random.choice(self.deity_possibilities)
        direction = self.random_wall(room)
        loc = self.broad_result_base.format(direction)

        # Create the Altar proper
        deco = Decoration(aliases=[self.broad_alias_base],
            broad_results=loc,
            inspect_results=self.inspect_results_base.format(deity))
        self.create_altar_top(room)
        room.add(deco)

    def create_altar_top(self, room):
        top = Container(['top of the altar', 'altar top'],\
            broad_results='',\
            inspect_results = 'The altar is in good condition')
        r = ModuleDecorator('erukar.game.inventory', self.generation_parameters)
        top.add(r.create_one())
