from erukar.engine.model.Describable import Describable
import functools, operator

class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    BaseName = 'base'
    EssentialPart = 'item part'
    Persistent = False

    def __init__(self, item_type='Item', name="Item"):
        self.item_type = item_type
        self.equipment_locations = []
        self.name = name
        self.price = 0
        self.description = Item.generic_description
        self.modifiers = []
        self.set_vision_results('You see a {BaseName}.','You see a {BaseName}.',(1,10))
        self.set_sensory_results('You sense a {BaseName}.','You sense a {BaseName}.',(5,20))
        self.set_detailed_results('There is a {BaseName}.', 'You see a {name}.')
        self.material = None

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

    def describe_modifiers(self, lifeform, acu, sen):
        modifier_descriptions = [x.on_inspect(lifeform, acu, sen) for x in self.modifiers if x.Description is not '']
        return ' ' + ' '.join(modifier_descriptions)

    def on_inspect(self, lifeform, acu, sen):
        modifiers = self.describe_modifiers(lifeform, acu, sen)
        material = '' if not self.material else self.material.on_inspect(lifeform, acu, sen)
        self_desc = self.describe_base(lifeform, acu, sen)
        if self_desc is '':
            return ''
        return self.mutate(' '.join(x for x in [self_desc, material, modifiers] if x is not ''))

    def describe_material(self):
        return self.material.BriefDescription if self.material else self.name
