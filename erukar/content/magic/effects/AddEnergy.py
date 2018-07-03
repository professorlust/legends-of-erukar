from erukar.system.engine import MagicEffect
from erukar.ext.nlg import Healing
import random


class AddEnergy(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        heal_range = AddEnergy.heal_range(**kwargs)
        heal_amount = random.randint(*heal_range)
        target.arcane_energy = min(target.maximum_arcane_energy(), target.arcane_energy + heal_amount)
        return Healing.quantified(instigator, heal_amount, 'energy'), kwargs

    def heal_range(**kwargs):
        if 'range' in kwargs and isinstance(kwargs['range'], tuple):
            return kwargs['range']
        return (10, 25)
