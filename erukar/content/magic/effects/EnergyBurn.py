from erukar.system.engine import MagicEffect, Lifeform


class EnergyBurn(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        percent = EnergyBurn.arg('percent', 0.05, float, **kwargs)
        power = EnergyBurn.arg('power', 5.0, float, **kwargs)
        damage_type = EnergyBurn.arg('damage_type', 'arcane', str, **kwargs)
        actual_energy = self.actual_energy(target, percent)
        if actual_energy <= 0:
            return 'Energy burn failed!', kwargs
        burn = int(actual_energy * power)
        target.arcane_energy -= actual_energy
        result = target.apply_damage(instigator, None, [
            (burn, damage_type)
        ])
        damage_str = ', '.join('{} {}'.format(*x) for x in result['post_mitigation'])
        log = 'You inflict {} damage on {}, burning {} energy!'.format(
            damage_str,
            target.alias(),
            actual_energy)
        return log, kwargs

    def actual_energy(self, target, percent):
        if not isinstance(target, Lifeform):
            return 0
        max_amount = int(max(0.0, target.maximum_arcane_energy() * percent))
        return target.arcane_energy\
            if max_amount > target.arcane_energy\
            else max_amount
