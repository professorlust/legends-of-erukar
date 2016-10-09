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


    def __init__(self, name, damage_range, mod, dist_and_params):
        self.name = name
        self.damage = damage_range
        self.modifier = mod
        self.distribution, self.dist_params = dist_and_params

    def roll(self, attacker):
        random_val = self.distribution(*self.dist_params)
        raw = np.round((self.damage[1] - self.damage[0]) * random_val) + self.damage[0]
        if hasattr(attacker, self.modifier):
            return int(raw) + getattr(attacker, self.modifier)
        return int(raw)

    @staticmethod
    def actual_damage_values(instigator, enemy, weapon, damages):
        for damage_amount, damage_type in damages:
            if enemy.deflection(damage_type) >= damage_amount:
                continue
            actual_damage = int(enemy.mitigation(damage_type) * damage_amount)
            damage_taken_by_armor = damage_amount - actual_damage
            if weapon is not None:
                weapon.take_damage(damage_taken_by_armor)
            enemy.damage_armor(damage_taken_by_armor)
            if actual_damage > 0:
               yield (actual_damage, damage_type)

    @staticmethod
    def deflections(instigator, enemy, weapon, damages):
        for damage_amount, damage_type in damages:
            if enemy.deflection(damage_type) >= damage_amount:
                yield damage_type
