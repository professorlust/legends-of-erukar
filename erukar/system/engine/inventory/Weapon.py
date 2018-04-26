from .Item import Item
import erukar, random
import numpy as np

class Weapon(Item):
    Persistent = True
    BaseName = "Weapon"
    EssentialPart = "weapon"
    MaximumRange = 4
    RangePenalty = 5
    EquipmentLocations = ['right','left']

    DamageVariance        = 0.50
    RawBase               = 10
    ScalingRequirement = 8

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    SuccessfullyAttackWith = 'Your attack hits {target}!'
    YouAreHitBy = 'You are hit by {subject}\'s {weapon_name}!'

    # Used when you need to have projectiles
    Variant = 'weapon' 
    RequiresAmmo = False
    AmmoType = ''
    BaseVariance = 0.8

    def __init__(self, modifiers=None):
        super().__init__(self.BaseName,modifiers=modifiers)
        self.name = self.BaseName
        self.item_type = "weapon"
        self.damages = []

    def equipment_slots(self, lifeform):
        return lifeform.weapon_slots()

    def on_calculate_attack(self, attack_cmd):
        '''Needs implementation''' 
        pass

    def on_calculate_attack_roll(self, base_attack_roll, attacker, target):
        return base_attack_roll

    def has_correct_ammo(self, ammo):
        return isinstance(ammo, getattr(erukar.content.inventory.ammunition, self.AmmoType))

    def calculate_damage(self, attacker):
        calculated = {}
        for damage in self.get_damages():
            scaled = list(self.vary_damage(attacker, damage.scalars))
            calculated[damage.damage_type] = int(sum([amt for amt,dt in scaled]))
        return [(calculated[dt],dt) for dt in calculated]

    def vary_damage(self, attacker, scalars):
         for scalar in scalars:
             actual_variance = random.uniform(self.lower_variance(attacker), self.upper_variance(attacker))
             yield (scalar.scale_for(attacker) * actual_variance, actual_variance)

    def variance(self, attacker=None):
        return self.BaseVariance

    def lower_variance(self, caller=None):
        return 1.0-self.variance()
    def upper_variance(self, caller=None):
        return 1.0+self.variance()

    def on_process_damage(self, attack_state, command):
        for modifier in self.modifiers:
            modifier.on_process_damage(attack_state, command)

    def on_inventory(self):
        return '{} ({}%)'.format(self.format(), int(100*self.durability_coefficient))

    def failing_requirements(self, wielder):
        return []

    def on_inventory_inspect(self, lifeform):
        scale = self.efficacy_for(lifeform)
        name = '{} ({} / {})'.format(self.format(), int(self.durability()), int(self.max_durability()))
        damage_desc = self.damage_inspection(lifeform)
        weight_desc = '{:>11} {:12}: {:3.2f} levts'.format('+', 'Weight:', self.weight())
        mods = ([self.material] + self.modifiers) if self.material else self.modifiers
        mod_desc = '\n'.join(['{:>11} {}: {}'.format('•',d.InventoryName, d.mutate(d.InventoryDescription)) for d in mods])
        return '\n'.join([name, weight_desc, damage_desc, mod_desc])

    def attack_range(self, lifeform):
        return self.MaximumRange

    def get_damages(self):
        for damage in self.get_base_damages():
            for modifier in self.modifiers:
                modifier.modify_base_damage(damage, self)
            yield damage
        for modifier in self.modifiers:
            gen = modifier.get_additional_damages(self)
            if gen is not None:
                yield from gen

    def get_base_damages(self):
        pass

    def damage_inspection(self, lifeform):
        descriptions = []
        for damage in self.get_damages():
            d_type = '{}Percentage'.format(damage.damage_type.capitalize())
            if hasattr(d_type, self):
                descriptions.append(self.inspect_percentage_damage(damage, lifeform, d_type))
                continue
            descriptions.append(self.inspect_normal_damage(damage, lifeform))
        joined = ', '.join(descriptions)
        return 'This {} deals damage distributed as follows: {}'.format(self.alias(), joined)

    def inspect_normal_damage(self, damage, lifeform):
        raw = damage.raw_scaled_for(lifeform)
        low = self.lower_variance() * raw
        high = self.upper_variance() * raw
        return '{} ({} to {})'.format(damage.damage_type, low, high)

    def generate_damage_details_for_inventory(self, caller):
        for damage in self.get_damages():
            raw = damage.raw_scaled_for(caller)
            result = {
                'type': damage.damage_type,
                'raw': int(raw),
                'low': int(self.lower_variance() * raw),
                'high': int(self.upper_variance() * raw)
            }
            percent_string = '{}Percentage'.format(damage.damage_type.capitalize())
            if hasattr(self, percent_string):
                result['percent'] = int(getattr(self, percent_string, 0.0) * 100)
            yield result

    def inspect_percentage_damage(self, damage, lifeform, percent_string):
        percentage = getattr(self, percent_string, 0.0) * 100.0
        raw = damage.raw_scaled_for(lifeform)
        low = self.lower_variance() * raw
        high = self.upper_variance() * raw
        return '{:0.0f}% {} ({} to {})'.format(percentage, damage.damage_type, low, high)
