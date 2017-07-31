from erukar.system.engine import Describable, Rarity
from erukar.ext.math import Curves
import functools, operator, math

class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    IsInteractible = True
    BaseName = 'base'
    InventoryDescription = "inv description"
    EssentialPart = 'item part'
    SupportPart = 'item part'
    Persistent = False
    PersistentAttributes = ['durability_coefficient']

    MaxDurability = 100
    BaseWeight = 0 # In Pounds
    BasePrice = 10
    EquipmentLocations = []

    RequiresTwoHands = False
    ActionPointCostToEquip = 1
    ActionPointCostToUnequip = 1

    '''
    Stat scaling is a linear relationship between a specific attribute and the scaling_factor
    The Damage Range is essentially a proportion
    
    # Assuming damage range is 1 to 4
    # 'strength': { 'requirement': 20, 'cutoff': 200, 'scaling_factor': 1.5 }
    @ str = 15,  damage = damage * 15/20            = 0.75 * damage          =   1 to   3
    @ str = 20,  damage = damage * 20/20            = 1.0 * damage           =   1 to   4
    @ str = 30,  damage = damage + (30 - 20) * 1.5  = damage +  15 + STR-req =  21 to  34
    @ str = 60,  damage = damage + (60 - 20) * 1.5  = damage +  60 + STR-req =  81 to 124
    @ str = 200, damage = damage + 180 * 1.5        = damage + 270 + STR-req = 361 to 574
    @ str = 260, damage = damage + 180 * 1.5        = damage + 270 + STR-req = 391 to 694

    In the event of multiple stat influences, 

    It can, however, be an s-curve if you specify 's-curve': True as in below
    # 'strength': { 'requirement': 20, 'cutoff': 200, 'scaling_factor': 1.5, 's-curve': True }
    '''
    BaseStatInfluences = {
    }

    def __init__(self, item_type='Item', name="Item", modifiers=None):
        super().__init__()
        self.stat_influences = self.BaseStatInfluences
        self.item_type = item_type
        self.owner = None
        self.name = name
        self.description = Item.generic_description
        self.durability_coefficient = 1

        # Modifiers
        self.material = None
        self.build_quality = None
        self.size = None
        self.modifiers = []

        if modifiers:
            for modifier in modifiers:
                modifier().apply_to(self)

    def equipment_slots(self, lifeform):
        return self.EquipmentLocations

    def rarity(self):
        full_mod_list = self.modifiers + [self.material]
        if not any([x for x in full_mod_list if x]):
            return Rarity.Mundane
        max_rarity = max([x.rarity.value for x in full_mod_list])
        return Rarity(max_rarity)

    def efficacy_for(self, lifeform):
        return 1.0, 0

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

    def weight(self):
        mults = [x.WeightMultiplier for x in self.modifiers]
        if hasattr(self, 'material') and self.material:
            return functools.reduce(operator.mul, mults, self.BaseWeight * self.material.WeightMultiplier)
        return functools.reduce(operator.mul, mults, self.BaseWeight)

    def price(self):
        mults = [x.PriceMultiplier for x in self.modifiers]
        if hasattr(self, 'material') and self.material:
            return functools.reduce(operator.mul, mults, self.BasePrice * self.material.PriceMultiplier * self.durability_multiplier())
        return functools.reduce(operator.mul, mults, self.BasePrice)

    def durability_multiplier(self):
        mmdpm = self.material.MinimumDurabilityPriceMultiplier
        return (1 - mmdpm) * pow(self.durability(), 2) / pow(self.max_durability(), 2)  + mmdpm

    def alias(self):
        alias = self.name if not self.material else self.material.on_alias(self.name)
        for mod in self.modifiers:
            alias = mod.on_alias(alias)
        return alias

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
            return self.alias()
        # show price
        return '({} R)'.format(self.alias(), int(self.price()))

    def attack_range(self, lifeform):
        return 0
