from erukar.system.engine import MagicEffect


class InflictDamage(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        power = InflictDamage.arg('power', 5.0, float, **kwargs)
        damage_type = InflictDamage.arg('damage_type', 'arcane', str, **kwargs)
        result = target.apply_damage(instigator, None, [
            (power, damage_type)
        ])
        damage_str = ', '.join('{} {}'.format(*x) for x in result['post_mitigation'])
        log = 'You inflict {} damage on {}'.format(
            damage_str,
            target.alias())
        return log, kwargs
