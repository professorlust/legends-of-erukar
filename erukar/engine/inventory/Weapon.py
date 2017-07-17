from .Item import Item
from erukar.engine.model.Damage import Damage
import erukar
import numpy as np

class Weapon(Item):
    Persistent = True
    BaseName = "Weapon"
    EssentialPart = "weapon"
    MaximumRange = 4
    RangePenalty = 5
    EquipmentLocations = ['right','left']

    DamageRange = [1, 2]
    DamageType = "ambiguous"
    DamageModifier = ""

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    SuccessfullyAttackWith = 'Your attack hits {target}!'
    YouAreHitBy = 'You are hit by {subject}\'s {weapon_name}!'

    # Used when you need to have projectiles
    RequiresAmmo = False
    AmmoType = ''

    def __init__(self, modifiers=None):
        super().__init__(self.BaseName,modifiers=modifiers)
        self.name = self.BaseName
        self.item_type = "weapon"
        self.damages = [Damage(
            self.DamageType, 
            list(self.DamageRange), 
            self.DamageModifier,
            (self.Distribution, self.DistributionProperties), 
            scales=True
        )]

    def equipment_slots(self, lifeform):
        return lifeform.weapon_slots()

    def on_calculate_attack(self, attack_cmd):
        '''Needs implementation''' 
        pass
#       if self.RequiresAmmo and attack_state.ammunition:
#           # This should mutate an AttackParameters object 
#           attack_state.ammunition.on_calculate_attack(attack_state)
#           attack_state.ammunition.consume()
#       super().on_attack(attack_state.attacker)

    def on_calculate_attack_roll(self, base_attack_roll, attacker, target):
        return base_attack_roll

    def has_correct_ammo(self, ammo):
        return isinstance(ammo, getattr(erukar.game.inventory.ammunition, self.AmmoType))

    def roll(self, attacker):
        scalar, offset = self.efficacy_for(attacker)
        return [self.rolled_damage(d, attacker) for d in self.damages]

    def rolled_damage(self, damage, attacker):
        '''used to get processed result for a single damage type'''
        return int(np.random.uniform(*damage.scaled_values(attacker))), damage.name

#   def on_calculate_attack_roll(self, raw, target):
#       result = raw
#       if self.material:
#           result = self.material.on_calculate_attack_roll(result, target)
#       for modifier in self.modifiers:
#           result = modifier.on_calculate_attack_roll(result, target) 
#       return result

    def on_process_damage(self, attack_state, command):
        for modifier in self.modifiers:
            modifier.on_process_damage(attack_state, command)

    def on_inventory(self):
        return '{} ({}%)'.format(self.format(), int(100*self.durability_coefficient))

    def on_inventory_inspect(self, lifeform):
        scale = self.efficacy_for(lifeform)
        mod = lifeform.get(self.DamageModifier)
        name = '{} ({} / {})'.format(self.format(), int(self.durability()), int(self.max_durability()))
        damage_desc = '\n'.join([self.damage_inspection(d, lifeform) for d in self.damages])
        weight_desc = '{:>11} {:12}: {:3.2f} levts'.format('+', 'Weight:', self.weight())
        mods = ([self.material] + self.modifiers) if self.material else self.modifiers
        mod_desc = '\n'.join(['{:>11} {}: {}'.format('•',d.InventoryName, d.mutate(d.InventoryDescription)) for d in mods])
        return '\n'.join([name, weight_desc, damage_desc, mod_desc])

    def damage_inspection(self, damage, lifeform):
        scale, offset = self.efficacy_for(lifeform)
        if damage.scales:
            mod = lifeform.get(damage.modifier)
            min_d = mod + offset + damage.damage[0] * scale
            max_d = mod + offset + damage.damage[1] * scale
        else:
            min_d = damage.damage[0]
            max_d = damage.damage[1]
        return '{:>11} {} to {} {} Damage'.format('•', int(min_d), int(max_d), damage.name.capitalize())
