from ..templates.Elemental import Elemental
import random

class IceElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'ice': (1, 0),
        'fire': (-0.5, 0)
    }
    
    def __init__(self):
        super().__init__('Ice Elemental', True)
        self.define_level(random.random()*20+5)
