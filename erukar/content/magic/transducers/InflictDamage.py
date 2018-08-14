from erukar.system.engine import Transducer
import random


class InflictDamage(Transducer):
    SuccessSelf = 'You inflict {} damage to yourself!'
    SuccessTarget = '{} inflicts {} damage upon you!'
    SuccessInstigator = 'You inflict {} damage upon {}!'

    def transduce(self, instigator, target, cmd, mutator):
        if target is not instigator and not mutator.evasion:
            cmd.log(target, 'No projectile created for this spell!')
            cmd.log(instigator, 'No projectile created for this spell!')
            return mutator
        damage_type = mutator.get('damage_type', 'arcane')
        damage = {}
        damage[damage_type] = random.uniform(*mutator.power_range(7.5, 15.0))
        result = target.apply_damage(instigator, None, damage)
        self.append_results(cmd, instigator, target, result['post_mitigation'])
        return mutator

    def append_results(self, cmd, instigator, target, damages):
        damage = ', '.join('{} {}'.format(int(damages[k]), k) for k in damages)
        if instigator is target:
            cmd.log(target.uid, self.SuccessSelf.format(damage))
            return
        # Instigator result
        cmd.log(instigator, self.SuccessInstigator.format(
            damage,
            target.alias()
        ))
        # Target result
        cmd.log(target, self.SuccessTarget.format(
            instigator.alias(),
            damage
        ))
