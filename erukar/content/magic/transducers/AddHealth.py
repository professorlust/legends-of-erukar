from erukar.system.engine import Transducer
from erukar.ext.nlg import Healing
import random


class AddHealth(Transducer):
    def transduce(self, instigator, target, cmd, mutator):
        heal_range = mutator.power_range(4, 10)
        amount = random.randint(*heal_range)
        target.health = min(target.maximum_health(), target.health + amount)
        result_str = Healing.quantified(instigator, amount, 'health')
        cmd.log(target, result_str)
        return mutator
