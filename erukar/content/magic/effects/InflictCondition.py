from erukar.system.engine import MagicEffect
import erukar


class InflictCondition(MagicEffect):
    def enact(self, instigator, target, **kwargs):
        condition = InflictCondition.get_condition(**kwargs)
        condition(target, instigator)
        log = 'You receive the {} condition temporarily'.format(condition.Noun)
        return log, kwargs

    def get_condition(**kwargs):
        if 'type' in kwargs and isinstance(kwargs['type'], type):
            return kwargs['type']
        return erukar.content.conditions.Bolstered
