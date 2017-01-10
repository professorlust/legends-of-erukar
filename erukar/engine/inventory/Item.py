from erukar.engine.model.Describable import Describable
from erukar.engine.calculators.Curves import Curves
import functools, operator

class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    IsInteractible = True
    BaseName = 'base'
    EssentialPart = 'item part'
    SupportPart = 'item part'
    Persistent = False
    PersistentAttributes = ['durability_coefficient']

    MaxDurability = 100
    StandardWeight = 0 # In Pounds
    BasePrice = 10
    EquipmentLocations = []
    BaseStatInfluences = {
        # Determines the influence of stats on the Item's efficacy. These totals are
        # multiplicative. See efficacy_for method for more details.
        # Uses the following format
        # 'strength': { 'requirement': 20, 'scaling_factor': 1.5, 'max_scale': 2 }
    }

    def __init__(self, item_type='Item', name="Item"):
        self.stat_influences = self.BaseStatInfluences
        self.item_type = item_type
        self.owner = None
        self.name = name
        self.description = Item.generic_description
        self.modifiers = []
        self.durability_coefficient = 1
        self.material = None

    def efficacy_for(self, lifeform):
        total = 1.0
        for stat in self.stat_influences:
            value = lifeform.calculate_effective_stat(stat)
            total *= Curves.item_stat_efficacy(value, **self.stat_influences[stat])
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
        return self.format()

    def on_inventory_inspect(self, lifeform):
        return self.on_inventory()

    def on_unequip(self, lifeform):
        for modifier in self.modifiers:
            modifier.on_unequip(lifeform)

    def on_equip(self, lifeform):
        for modifier in self.modifiers:
            modifier.on_equip(lifeform)

    def durability(self):
        return self.durability_coefficient * self.max_durability() 

    def max_durability(self):
        return self.material.DurabilityMultiplier * self.MaxDurability

    def price(self):
        prices = [x.PriceMultiplier for x in self.modifiers]
        if hasattr(self, 'material') and self.material:
            return functools.reduce(operator.mul, prices, self.BasePrice * self.material.PriceMultiplier * self.durability_multiplier())
        return functools.reduce(operator.mul, prices, self.BasePrice)

    def durability_multiplier(self):
        mmdpm = self.material.MinimumDurabilityPriceMultiplier
        return (1 - mmdpm) * pow(self.durability(), 2) / pow(self.max_durability(), 2)  + mmdpm

    def alias(self):
        return self.name

    def belongs_in_hand(self, lifeform):
        return any(set(lifeform.attack_slots).intersection(set(self.EquipmentLocations)))

    def calculate_desireability(self):
        return functools.reduce(operator.mul, [mod.Desirability for mod in self.modifiers])

    def on_inspect(self, lifeform, acuity, sense):
        mods = [x.on_inspect(lifeform,acuity,sense) for x in [self.material] + self.modifiers if x is not None]
        pre_mutation = super().on_inspect(lifeform,acuity,sense) + ' ' + Describable.erjoin([x for x in mods if x is not ''])
        return self.mutate(pre_mutation.strip())

    def on_glance(self, lifeform, acuity, sense):
        mods = [x.on_glance(lifeform,acuity,sense) for x in [self.material] + self.modifiers if x is not None]
        pre_mutation = '~a_or_an~ ' + self.name + ' ' + Describable.erjoin([x for x in mods if x is not ''])
        return self.mutate(pre_mutation.strip())

    def persistable_attributes(self):
        '''For use with database; getattrs all attributes defined by persistent_attr dict'''
        return {pattr: getattr(self, pattr) for pattr in self.PersistentAttributes if hasattr(self, pattr)}

    def take_damage(self, amount):
        self.durability_coefficient = max(0, self.durability() - amount) / self.max_durability()

    def format(self, with_price=False):
        if not with_price:
            if hasattr(self, 'material') and self.material:
                return '{} {}'.format(self.material.InventoryName, self.alias())
            return self.alias()
        # show price
        if hasattr(self, 'material') and self.material:
            return '{} {} ({} R)'.format(self.material.InventoryName, self.alias(), int(self.price()))
        return '{} ({} R)'.format(self.alias(), int(self.price()))
