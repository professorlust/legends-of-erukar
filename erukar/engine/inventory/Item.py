from erukar.engine.model.Describable import Describable
import functools, operator

class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    BaseName = 'base'
    EssentialPart = 'item part'

    def __init__(self, item_type='Item', name="Item"):
        self.item_type = item_type
        self.equipment_locations = []
        self.name = name
        self.price = 0
        self.description = Item.generic_description
        self.modifiers = []
        self.set_vision_results('You see a {name}.','You see a {alias}.',(0,1))
        self.set_sensory_results('You sense a {name}.','You sense a {alias}.',(50,60))

    def describe(self):
        return self.name

    def matches(self, other):
        return other.lower() in self.alias().lower() \
            or other.lower() in self.item_type.lower()

    def on_inventory(self, *_):
        return self.alias()

    def alias(self):
        return self.name

    def belongs_in_hand(self):
        return 'left' in self.equipment_locations or 'right' in self.equipment_locations

    def calculate_desireability(self):
        return functools.reduce(operator.mul, [mod.Desirability for mod in self.modifiers])

    def on_inspect(self, lifeform, acu, sen):
        modifier_descriptions = [x.Description for x in self.modifiers if x.Description is not '']
        if len(modifier_descriptions) > 0:
            return self.mutate(self.describe_base(lifeform, acu, sen) + '. ' +' '.join(modifier_descriptions))
        return self.describe_base(lifeform, acu, sen)
