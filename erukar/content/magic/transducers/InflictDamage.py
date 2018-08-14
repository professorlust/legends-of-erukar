from erukar.system.engine import Transducer
import random


class InflictDamage(Transducer):
    SuccessSelf = 'You inflict {} damage to yourself!'
    SuccessTarget = '{} inflicts {} damage upon you!'
    SuccessInstigator = 'You inflict {} damage upon {}!'

    def transduce(self, caster, target, cmd, mutator):
        if target is not caster and not mutator.was_evaded:
            cmd.log(target, 'No projectile created for this spell!')
            cmd.log(caster, 'No projectile created for this spell!')
            return mutator
        _evaded = mutator.was_evaded
        evaded = _evaded(caster, target, cmd, mutator)
        if evaded:
            mutator.append_evasion_results(caster, target, cmd, mutator)
            return mutator
        damage_type = mutator.get('damage_type', 'arcane')
        damage = {}
        damage[damage_type] = random.uniform(*mutator.power_range(7.5, 15.0))
        result = target.apply_damage(caster, None, damage)
        self.append_results(cmd, caster, target, result['post_mitigation'])
        return mutator

    def append_results(self, cmd, caster, target, damages):
        damage = ', '.join('{} {}'.format(int(damages[k]), k) for k in damages)
        if caster is target:
            cmd.log(target.uid, self.SuccessSelf.format(damage))
            return
        # Instigator result
        cmd.log(caster, self.SuccessInstigator.format(
            damage,
            target.alias()
        ))
        # Target result
        cmd.log(target, self.SuccessTarget.format(
            caster.alias(),
            damage
        ))
