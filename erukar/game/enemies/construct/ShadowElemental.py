from erukar.game.enemies.templates.Elemental import Elemental
from erukar.game.modifiers.inventory.random.Unholy import Unholy
import random

class ShadowElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'demonic': (1, 0),
        'divine': (-0.5, 0)
    }

    def __init__(self, actual_name, is_random=True):
        super().__init__(actual_name, is_random)
        self.define_level(random.random()*20+5)
        
    def apply_elemental_effects(self):
        Unholy().apply_to(self.left)
        Unholy().apply_to(self.right)

