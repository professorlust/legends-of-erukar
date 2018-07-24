from erukar.system.engine import ErukarActor, Rarity
from erukar.ext.math import Curves
import functools
import operator


class Item(ErukarActor):
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

        # Modifiers
        self.material = None
        self.build_quality = None
        self.size = None
        self.modifiers = []

        if modifiers:
            for modifier_type in modifiers:
                modifier_type().apply_to(self)

    def generate_tile(self, dimensions, tile_id):
        h, w = dimensions
        for y in range(h):
            for x in range(w):
                if not (int(h/4) < y < int(3*h/4)):
                    yield {'r': 0, 'g': 0, 'b': 0, 'a': 0}
                    continue
                if not (int(h/4) < x < int(3*h/4)):
                    yield {'r': 0, 'g': 0, 'b': 0, 'a': 0}
                    continue
                if (x > w/2 and x > y) or (x <= w/2 and y > x):
                    yield {'r': 245, 'g': 245, 'b': 220, 'a': 1}
                    continue
                yield {'r': 0, 'g': 0, 'b': 0, 'a': 0}

    def durability_coefficient(self):
        return self.durability / self.total_durability()

    def total_durability(self):
        mutator_name = 'modify_total_durability'
        return self.modify_element(mutator_name, self.MaxDurability)

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

    def tick(self, cmd, owner):
        for modifier in self.modifiers:
            modifier.tick(cmd, owner)

    def matches(self, other):
        return other.lower() in self.alias().lower() \
            or other.lower() in self.item_type.lower()

    def on_start(self, dungeon):
        for modifier in self.modifiers:
            modifier.on_start(dungeon)
        if not hasattr(self, 'durability'):
            self.durability = self.total_durability()

    def on_take(self, cmd, taker=None):
        self.owner = taker or cmd.args['player_lifeform']
        for modifier in self.modifiers:
            modifier.on_take(taker)

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
        dur_coeff = pow(self.durability(), 2) / pow(self.total_durability(), 2)
        return (1 - mmdpm) * dur_coeff  + mmdpm

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
        self.durability_coefficient = gg

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

    def modify_element(self, mod_name, _el, cmd=None):
        for mod in self.modifiers:
            if hasattr(mod, mod_name):
                _el = getattr(mod, mod_name)(_el, cmd) or _el
        return _el

    def post_successful_attack(self, cmd, attacker, weapon, target):
        for modifier in self.modifiers:
            modifier.post_successful_attack(cmd, attacker, weapon, target)

    def post_missed_attack(self, cmd, attacker, weapon, target):
        for modifier in self.modifiers:
            modifier.post_missed_attack(cmd, attacker, weapon, target)
