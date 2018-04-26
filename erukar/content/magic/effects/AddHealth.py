from erukar.system.engine import MagicEffect
from erukar.ext.nlg import Healing
import random

class AddHealth(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        heal_range = AddHealth.heal_range(**kwargs)
        heal_amount = random.randint(*heal_range)
        target.health = min(target.max_health, target.health + heal_amount)
        return Healing.quantified(instigator, heal_amount, 'health')

    def heal_range(**kwargs):
        if 'range' in kwargs and isinstance(kwargs['range'], tuple):
            return kwargs['range']
        return (10, 25)
