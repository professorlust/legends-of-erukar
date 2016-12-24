from erukar.game.enemies.templates.Elemental import Elemental
from erukar.game.modifiers.inventory.random.Flaming import Flaming
import random

class FireElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'fire': (1, 0),
        'ice': (-0.5, 0)
    }

    def __init__(self, actual_name, is_random=True):
        super().__init__(actual_name, is_random)
        self.define_level(random.random()*20+5)
        
    def apply_elemental_effects(self):
        Flaming().apply_to(self.left)
        Flaming().apply_to(self.right)
