from erukar.system.engine import Transducer
import random


class InflictDamage(Transducer):
    SuccessTarget = 'You take {} damage.'
    SuccessCaster = '{} takes {} damage.'

    def transduce(self, caster, target, cmd, mutator):
        if target is not caster and not mutator.was_evaded:
            cmd.log(caster, 'No projectile created for this spell!')
            return mutator
        evaded = mutator.was_evaded(mutator, caster, target, cmd)
        if evaded:
            return mutator
        damage_type = mutator.get('damage_type', 'arcane')
        damage = {}
        damage[damage_type] = random.uniform(*mutator.power_range(7.5, 15.0))
        result = target.apply_damage(caster, None, damage)
        self.append_results(cmd, caster, target, result['post_mitigation'])
        return mutator

    def append_results(self, cmd, caster, target, damages):
        damage = ', '.join('{} {}'.format(int(damages[k]), k) for k in damages)
        if caster is not target:
            cmd.log(caster, self.SuccessCaster.format(target.alias(), damage))
        cmd.log(target, self.SuccessTarget.format(caster.alias(), damage))
