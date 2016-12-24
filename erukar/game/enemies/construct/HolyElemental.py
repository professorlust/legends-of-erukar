from erukar.game.enemies.templates.Elemental import Elemental
from erukar.game.modifiers.inventory.random.Holy import Holy
import random

class HolyElemental(Elemental):
    BaseDamageMitigations = {
        'piercing': (0.45, 2),
        'slashing': (0.30, 2),
        'bludgeoning': (0.70, 3),
        'divine': (1, 0),
        'demonic': (-0.5, 0)
    }

    def __init__(self, actual_name, is_random=True):
        super().__init__(actual_name, is_random)
        self.define_level(random.random()*20+5)
        
    def apply_elemental_effects(self):
        Holy().apply_to(self.left)
        Holy().apply_to(self.right)

