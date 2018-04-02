from ..templates.Elemental import Elemental
import random

class AcidElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'acid': (1, 0),
        'electric': (-0.5, 0)
    }

    def __init__(self):
        super().__init__('Acid Elemental', True)
        self.define_level(int(random.random())*20+5)
