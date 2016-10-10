from erukar.engine.model.Describable import Describable
import functools, operator

class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    BaseName = 'base'
    BriefDescription = "You see a {BaseName}"
    EssentialPart = 'item part'
    SupportPart = 'item part'
    Persistent = False
    PersistentAttributes = ['durability']

    MaxDurability = 100
    StandardWeight = 0 # In Pounds
    EquipmentLocations = []
    StatInfluences = {
        # Determines the influence of stats on the Item's efficacy. These totals are
        # multiplicative. See efficacy_for method for more details.
        # Uses the following format
        # 'strength': { 'requirement': 20, 'scaling': 1.5, 'max_scale': 2 }
    }

    def __init__(self, item_type='Item', name="Item"):
        self.item_type = item_type
        self.owner = None
        self.name = name
        self.price = 0
        self.description = Item.generic_description
        self.modifiers = []
        self.durability = self.MaxDurability
        self.set_vision_results('You see a {BaseName}.','You see a {BaseName}.',(1,10))
        self.set_sensory_results('You sense a {BaseName}.','You sense a {BaseName}.',(5,20))
        self.set_detailed_results('There is a {BaseName}.', 'You see a {name}.')
        self.material = None

    def efficacy_for(self, lifeform):
        total = 1.0
        for stat in self.StatInfluences:
            value = lifeform.calculate_effective_stat(stat)
            total *= Curves.item_stat_efficacy(value, **self.StatInfluences[stat])
        return total

    def describe(self):
        return self.name

    def tick(self):
        pass

    def matches(self, other):
        return other.lower() in self.alias().lower() \
            or other.lower() in self.item_type.lower()

    def on_start(self, room):
        for modifier in self.modifiers:
            modifier.on_start(room)

    def on_take(self, lifeform):
        self.owner = lifeform
        for modifier in self.modifiers:
            modifier.on_take(lifeform)

    def on_drop(self, room, lifeform):
        self.owner = None
        for modifier in self.modifiers:
            modifier.on_drop(room, lifeform)

    def on_move(self, room):
        for modifier in self.modifiers:
            modifier.on_move(room)

    def on_inventory(self, *_):
        return self.alias()

    def on_inventory_inspect(self):
        return self.on_inventory()

    def on_unequip(self, lifeform):
        for modifier in self.modifiers:
            modifier.on_unequip(lifeform)

    def on_equip(self, lifeform):
        for modifier in self.modifiers:
            modifier.on_equip(lifeform)

    def alias(self):
        return self.name

    def belongs_in_hand(self, lifeform):
        return any(set(lifeform.attack_slots).intersection(set(self.EquipmentLocations)))

    def calculate_desireability(self):
        return functools.reduce(operator.mul, [mod.Desirability for mod in self.modifiers])

    def describe_modifiers(self, lifeform, acu, sen):
        modifier_descriptions = [x.on_inspect(lifeform, acu, sen) for x in self.modifiers]
        return ' ' + ' '.join(modifier_descriptions)

    def describe_brief_modifiers(self, lifeform, acu, sen):
        modifier_descriptions = [x.brief_inspect(lifeform, acu, sen) for x in self.modifiers]
        return ' ' + ' '.join(modifier_descriptions)

    def on_inspect(self, lifeform, acu, sen):
        modifiers = self.describe_modifiers(lifeform, acu, sen)
        material = '' if not self.material else self.material.on_inspect(lifeform, acu, sen)
        self_desc = self.describe_base(lifeform, acu, sen)
        if self_desc is '':
            return ''
        return self.mutate(' '.join(x for x in [self_desc, material, modifiers] if x is not ''))

    def brief_inspect(self, lifeform, acuity, sense):
        if acuity < self.vision_range[0]:
            return ''
        material = self.BriefDescription if not self.material else self.material.brief_inspect(lifeform, acuity, sense)
        return self.mutate(material)

    def describe_material(self):
        return self.material.BriefDescription if self.material else self.name

    def persistable_attributes(self):
        '''For use with database; getattrs all attributes defined by persistent_attr dict'''
        return {pattr: getattr(self, pattr) for pattr in self.PersistentAttributes if hasattr(self, pattr)}

    def take_damage(self, amount):
        self.durability = max(0, self.durability - amount)
