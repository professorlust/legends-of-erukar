import numpy as np

class Damage:
    Types = [
        'piercing',
        'bludgeoning',
        'slashing',
        'fire',
        'ice',
        'electric',
        'acid',
        'force',
        'divine',
        'demonic',
    ]

    def __init__(self, name, damage_range, mod, dist_and_params, scales=False):
        self.scales = scales
        self.name = name
        self.damage = damage_range
        self.modifier = mod
        self.distribution, self.dist_params = dist_and_params
        self.requirement = 8
        self.max_scale = 100
        self.scalar = 2.5

    def roll(self, attacker):
        # Get a random value from the distribution passed in 
        random_val = self.distribution(*self.dist_params)
        # Scale the value between the boundary rangess
        raw = np.round((self.damage[1] - self.damage[0]) * random_val) + self.damage[0]
        # Do we have a modifier for this value? if so, apply it
        if hasattr(attacker, self.modifier) and self.scales:
            return int(raw) + getattr(attacker, self.modifier)
        return int(raw)

    def scaled_values(self, for_player):
        return self.scale(for_player, self.damage[0]), self.scale(for_player, self.damage[1])

    def scale(self, for_player, value):
        if not self.scales: return value
        stat = getattr(for_player, self.modifier)
        if stat < self.requirement: return 1
        return int((1+min(self.max_scale, (stat - self.requirement))) * self.scalar + value)

    @staticmethod
    def actual_damage_values(instigator, enemy, weapon, damages):
        '''Determine the actual damage amount dealt after deflection and mitigation'''
        for damage_amount, damage_type in damages:
            # Calculate the unmitigated damage
            actual_damage = int(enemy.mitigation(damage_type) * damage_amount)
            damage_taken_by_armor = int(damage_amount) - actual_damage
            # Mitigated damage is reflected back to the weapon if it exists
            if weapon is not None:
                weapon.take_damage(damage_taken_by_armor)
            enemy.damage_armor(damage_taken_by_armor)
            # After mitigation, if there is any remaining damage, the lifeform takes that in health
            if actual_damage > 0:
               yield (actual_damage, damage_type)

    @staticmethod
    def deflections(instigator, enemy, damages):
        for damage_amount, damage_type in damages:
            if hasattr(enemy, 'deflection') and enemy.deflection(damage_type) >= damage_amount:
                yield damage_type
