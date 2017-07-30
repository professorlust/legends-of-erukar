from ..templates.Dragon import Dragon

class BlueDragon(Dragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'ice': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Blue Dragon", random)
        self.define_level(15)
