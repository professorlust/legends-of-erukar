from erukar.system.engine import Transducer
import random


class InflictDamage(Transducer):
    SuccessSelf = 'You inflict {} damage to yourself!'
    SuccessTarget = '{} inflicts {} damage upon you!'
    SuccessInstigator = 'You inflict {} damage upon {}!'

    def transduce(self, instigator, target, cmd, mutator):
        damage_type = mutator.get('damage_type', 'arcane')
        damage = random.uniform(*mutator.power_range(3.5, 6.5))
        result = target.apply_damage(instigator, None, [
            (int(damage), damage_type)
        ])
        self.append_results(cmd, instigator, target, result['post_mitigation'])
        return mutator

    def append_results(self, cmd, instigator, target, damages):
        damage = ', '.join('{} {}'.format(*x) for x in damages)
        if instigator is target:
            cmd.log(target.uid, self.SuccessSelf.format(damage))
            return
        # Instigator result
        cmd.log(instigator, self.SuccessInstigator.format(
            damage,
            target.alias()
        ))
        # Target result
        cmd.log(target, self.SuccessInstigator.format(
            instigator.alias(),
            damage
        ))
