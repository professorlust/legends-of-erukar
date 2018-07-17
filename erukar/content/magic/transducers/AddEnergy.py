from erukar.system.engine import Transducer
from erukar.ext.nlg import Healing
import random


class AddEnergy(Transducer):
    def transduce(self, instigator, target, cmd, mutator):
        heal_range = mutator.power_range(5, 10)
        amount = int(random.uniform(*heal_range))
        target.arcane_energy = min(
            target.maximum_arcane_energy(),
            target.arcane_energy + amount
        )
        cmd.log(target, Healing.quantified(instigator, amount, 'energy'))
        return mutator
