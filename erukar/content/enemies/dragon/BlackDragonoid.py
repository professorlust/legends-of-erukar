from ..templates.Dragonoid import Dragonoid
import random

class BlackDragonoid(Dragonoid):
    BaseDamageMitigations = {
        'piercing': (0.05, 0),
        'slashing': (0.10, 0),
        'bludgeoning': (0.15, 0),
        'acid': (0.4, 0)
    }

    def __init__(self, random=True):
        super().__init__("Black Dragonoid", random)
