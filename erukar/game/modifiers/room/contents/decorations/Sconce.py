from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
import random

class Sconce(RoomModifier):
    Probability = 0
    ProbabilityFromFabrication = 0.25

    broad_alias_base = 'sconce'
    broad_result_base = 'A sconce hangs on the {} wall of the room.'
    inspect_results_base = 'There is a {} inside of the sconce.'

    torch_possibilities = [
        ('charred torch', 0.0),
        ('unlit torch', 0.0),
        ('dimly burning torch', 0.25),
        ('smoldering torch', 0.15),
        ('burning torch', 0.5),
        ('brightly burning torch', 0.8)]

    def apply_to(self, room):
        torch, brightness_adjustment = random.choice(self.torch_possibilities)
        direction = random.choice([x for x in room.connections])
        loc = self.broad_result_base.format(direction.name)
        if room.connections[direction].is_door():
            loc = loc + ', to the {} of the passageway'.format(random.choice(['left', 'right']))
        deco = Decoration(aliases=[self.broad_alias_base, torch],
            broad_results=loc,
            inspect_results=self.inspect_results_base.format(torch))
        room.luminosity = min(1.0, room.luminosity + brightness_adjustment)
        room.add(deco)
