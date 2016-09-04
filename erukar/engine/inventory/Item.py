from erukar.engine.model.RpgEntity import RpgEntity
import functools, operator

class Item(RpgEntity):
    generic_description = 'This is {0}, but it otherwise has no real description whatsoever'

    def __init__(self, item_type='Item', name="Item"):
        self.item_type = item_type
        self.equipment_locations = []
        self.name = name
        self.price = 0
        self.description = Item.generic_description
        self.modifiers = []
        self.set_vision_results('You see a {describe}.','You see a {describe}.',(0,1))
        self.set_sensory_results('You sense a {describe}.','You sense a {describe}.',(50,60))

    def describe(self):
        return self.alias()

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
