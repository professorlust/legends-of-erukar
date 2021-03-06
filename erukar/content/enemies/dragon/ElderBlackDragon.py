from ..templates.ElderDragon import ElderDragon

class ElderBlackDragon(ElderDragon):
    BaseDamageMitigations = {
        'piercing': (0.25, 0),
        'slashing': (0.60, 0),
        'bludgeoning': (0.50, 0),
        'acid': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Elder Black Dragon", random)
        self.define_level(32)
