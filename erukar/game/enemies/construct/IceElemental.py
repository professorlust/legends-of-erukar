from erukar.game.enemies.templates.Elemental import Elemental
import random

class IceElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'ice': (1, 0),
        'fire': (-0.5, 0)
    }
    
    def __init__(self, actual_name, is_random=True):
        super().__init__(actual_name, is_random)
        self.define_level(random.random()*20+5)
