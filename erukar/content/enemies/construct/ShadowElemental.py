from ..templates.Elemental import Elemental
import random

class ShadowElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'demonic': (1, 0),
        'divine': (-0.5, 0)
    }

    def __init__(self):
        super().__init__('Shadow Elemental', True)
        self.define_level(int(random.random())*20+5)
