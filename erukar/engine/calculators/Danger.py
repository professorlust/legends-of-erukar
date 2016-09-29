class Danger:
    scalars = {
        'strength': 1.0,
        'dexterity': 1.0,
        'vitality': 0.9,
        'acuity': 0.6,
        'sense': 0.5,
        'resolve': 0.6,
        'level': 1.0
    }

    def calculate_for(enemy):
        return sum([self.Scalars[x] * getattr(enemy, x) for x in scalars])
