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
