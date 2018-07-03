from erukar.system.engine import MagicEffect
import erukar


class AddMitigation(MagicEffect):
    DefaultType = 'fire'
    DefaultPercent = 0.05

    def enact(self, instigator, target, **kwargs):
        damage_type = AddMitigation.arg(
            'damage_type',
            AddMitigation.DefaultType,
            str,
            **kwargs)
        power = AddMitigation.arg(
            'percent',
            AddMitigation.DefaultPercent,
            float,
            **kwargs)
        condition_type = erukar.content.conditions.BonusMitigation
        condition = condition_type(target, instigator)
        condition.mitigation_amount = power
        condition.damage_type = damage_type
        log = 'You receive {} additional {} mitigation!'.format(power, damage_type)
        return log, kwargs
