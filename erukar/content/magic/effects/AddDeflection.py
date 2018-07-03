from erukar.system.engine import MagicEffect
import erukar


class AddDeflection(MagicEffect):
    DefaultType = 'fire'
    DefaultPower = 5.0

    def enact(self, instigator, target, **kwargs):
        damage_type = AddDeflection.arg(
            'damage_type',
            AddDeflection.DefaultType,
            str,
            **kwargs)
        power = AddDeflection.arg(
            'power',
            AddDeflection.DefaultPower,
            float,
            **kwargs)
        condition_type = erukar.content.conditions.BonusDeflection
        condition = condition_type(target, instigator)
        condition.deflection_amount = int(power)
        condition.damage_type = damage_type
        log = 'You receive {} additional {} deflection!'.format(int(power), damage_type)
        return log, kwargs
