from ..templates.ElderDragon import ElderDragon

class ElderOrangeDragon(ElderDragon):
    BaseDamageMitigations = {
        'piercing': (0.15, 0),
        'slashing': (0.40, 0),
        'bludgeoning': (0.30, 0),
        'acid': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Elder Orange Dragon", random)
        self.define_level(36)
