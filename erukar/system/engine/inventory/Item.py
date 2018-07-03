from erukar.system.engine import Describable, Rarity
from erukar.ext.math import Curves
import functools
import operator


class Item(Describable):
    generic_description = 'This is {BaseName}, but it otherwise has no real description whatsoever'
    IsInteractible = True
    BaseName = 'base'
    InventoryDescription = "inv description"
    EssentialPart = 'item part'
    SupportPart = 'item part'
    Persistent = False
    PersistentAttributes = ['durability']

    ModifierPath = ''
    MaxDurability = 100
    BaseWeight = 0 # In Pounds
    BasePrice = 10
    EquipmentLocations = []

    CannotDrop = False
    IsUsable = False
    RequiresTwoHands = False
    ActionPointCostToEquip = 1
    ActionPointCostToUnequip = 1

    def __init__(self, item_type='Item', name="Item", modifiers=None):
        super().__init__()
        self.item_type = item_type
        self.owner = None
        self.name = name
        self.description = Item.generic_description
        self.total_durability = 100
        self.durability = self.total_durability

        # Modifiers
        self.material = None
        self.build_quality = None
        self.size = None
        self.modifiers = []

        if modifiers:
            for modifier_type in modifiers:
                modifier_type().apply_to(self)

    def durability_coefficient(self):
        return self.durability / self.total_durability

    def equipment_slots(self, lifeform):
        return self.EquipmentLocations

    def rarity(self):
        full_mod_list = self.modifiers + [self.material]
        if not any([x for x in full_mod_list if x]):
            return Rarity.Mundane
        max_rarity = max([getattr(x, 'rarity', Rarity.Mundane).value for x in full_mod_list])
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

    def on_start(self, dungeon):
        for modifier in self.modifiers:
            modifier.on_start(dungeon)

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

    def price(self, econ=None):
        price = self.BasePrice
        for modifier in self.modifiers:
            price *= modifier.PriceMultiplier
        if hasattr(self, 'material'):
            return price * getattr(self.material, 'PriceMultiplier', 1.0)
        return price

    def base_price(self):
        return self.price()

    def durability_multiplier(self):
        mmdpm = self.material.MinimumDurabilityPriceMultiplier
        return (1 - mmdpm) * pow(self.durability(), 2) / pow(self.max_durability(), 2)  + mmdpm

    def alias(self):
        alias = self.name if not self.material else self.material.on_alias(self.name)
        for mod in self.modifiers:
            alias = mod.on_alias(alias)
        return alias

    def long_alias(self):
        return self.alias()

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

    @classmethod
    def split(cls, original, quantity):
        return original, None

    def flavor_text(self, player):
        return 'This is a generic item. Lorem ipsum dolor sit amet, consectetur adipiscing elit'

    def modify_element(self, mod_name, element):
        for mod in self.modifiers:
            if hasattr(mod, mod_name):
                element = getattr(mod, mod_name)(self, element)
        return element

    def post_successful_attack(self, cmd, attacker, weapon, target):
        for modifier in self.modifiers:
            modifier.post_successful_attack(cmd, attacker, weapon, target)

    def post_missed_attack(self, cmd, attacker, weapon, target):
        for modifier in self.modifiers:
            modifier.post_missed_attack(cmd, attacker, weapon, target)
