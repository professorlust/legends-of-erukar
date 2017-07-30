from ..templates.Dragonoid import Dragonoid

class RedDragonoid(Dragonoid):
    BaseDamageMitigations = {
        'piercing': (0.05, 0),
        'slashing': (0.10, 0),
        'bludgeoning': (0.15, 0),
        'fire': (0.4, 0)
    }

    def __init__(self, random=True):
        super().__init__("Red Dragonoid", random)
