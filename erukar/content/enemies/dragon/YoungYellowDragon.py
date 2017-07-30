from ..templates.YoungDragon import YoungDragon

class YoungYellowDragon(YoungDragon):
    BaseDamageMitigations = {
        'piercing': (0.10, 0),
        'slashing': (0.35, 0),
        'bludgeoning': (0.20, 0),
        'electric': (1, 0)
    }

    def __init__(self, random=True):
        super().__init__("Young Yellow Dragon", random)
        self.define_level(11)
