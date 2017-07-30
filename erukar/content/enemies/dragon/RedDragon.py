from ..templates.Dragon import Dragon

class RedDragon(Dragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'fire': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Red Dragon", random)
        self.define_level(15)
