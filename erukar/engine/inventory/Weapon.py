from .Item import Item
from erukar.engine.model.Damage import Damage
import numpy as np

class Weapon(Item):
    Persistent = True
    BaseName = "Weapon"
    EssentialPart = "weapon"
    AttackRange = 0 # Maximum number of rooms beyond our current room that we can reach
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

    def __init__(self):
        super().__init__(self.BaseName)
        self.name = self.BaseName
        self.item_type = "weapon"
        self.damages = [Damage(self.DamageType, list(self.DamageRange), self.DamageModifier,\
                               (self.Distribution, self.DistributionProperties), scales=True)]

    def on_attack(self, attacker):
        '''Needs implementation''' 
        if self.RequiresAmmo:
            # This should mutate an AttackParameters object 
            self.get_ammo(attacker).on_attack(self, attacker)            
        super().on_attack(attacker)

    def can_attack(self, attacker):
        return not self.RequiresAmmo or self.get_ammo() is not None

    def get_ammo(self, attacker):
        return self.attacker.ammunition

    def use_ammo(self, attacker):
        ammo = self.get_ammo(attacker)
        if ammo is None: return 'No ammo was found!'
        ammo.consume()

    def roll(self, attacker):
        efficacy = self.efficacy_for(attacker)
        return [(d.roll(attacker)*efficacy if d.scales else d.roll(attacker), d.name) for d in self.damages]

    def on_calculate_attack_roll(self, raw, target):
        result = raw
        if self.material:
            result = self.material.on_calculate_attack_roll(result, target)
        for modifier in self.modifiers:
            result = modifier.on_calculate_attack_roll(result, target) 
        return result

    def on_apply_damage(self, attack_state, command):
        for modifier in self.modifiers:
            modifier.on_apply_damage(attack_state, command)

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
        weapon_scale = self.efficacy_for(lifeform)
        if damage.scales:
            mod = lifeform.get(damage.modifier)
            min_d = mod + damage.damage[0] * weapon_scale
            max_d = mod + damage.damage[1] * weapon_scale
        else:
            min_d = damage.damage[0]
            max_d = damage.damage[1]
        return '{:>11} {} to {} {} Damage'.format('•', int(min_d), int(max_d), damage.name.capitalize())
