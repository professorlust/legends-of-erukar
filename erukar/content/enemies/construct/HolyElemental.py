from ..templates.Elemental import Elemental
import random

class HolyElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'divine': (1, 0),
        'demonic': (-0.5, 0)
    }

    def __init__(self):
        super().__init__('Holy Elemental', True)
        self.define_level(random.random()*20+5)
