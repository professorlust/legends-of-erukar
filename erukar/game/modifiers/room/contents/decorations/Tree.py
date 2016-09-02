from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random, collections

class Tree(RoomModifier):
    Probability = 0.00
    ProbabilityFromFabrication = -0.9
    ProbabilityFromAltitude = 0.2

    materials = [
        "ash",
        "birch",
        "cedar",
        "poplar",
        "walnut",
        "locust",
        "dogwood"
    ]

    ages = [
        "sapling",
        "seedling",
        "tree",
        "snag",
        "stump"
    ]

    fields = [ 
        'material',
        'age']

    broad_alias_base="{material} {age}"
    broad_result_base="There is a {age} {location}"
    inspect_result_base="This is a {material} {age}."

    def get_arguments(self, location):
        all_but_loc = super().get_arguments() 
        all_but_loc['location'] = location
        return all_but_loc

    def apply_to(self, room):
        try:
            location = 'to the ' + random.choice(list(room.wall_directions())).name
        except:
            location = 'in the center'
        arguments = self.get_arguments(location)
        deco = Decoration(aliases=[self.mutate(self.broad_alias_base, arguments)],
            broad_results=self.mutate(self.broad_result_base, arguments),
            inspect_results=self.mutate(self.inspect_result_base, arguments))
        room.add(deco) 
