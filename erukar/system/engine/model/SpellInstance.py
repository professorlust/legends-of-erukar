from .MagicEffect import MagicEffect


class SpellInstance:
    '''Class which is basically just a way for spells to
    maintain parity from effect to effect'''

    def __init__(self, chain=None):
        self.chain = chain if chain and isinstance(chain, list) else []

    def cmd_execute(self, cmd):
        if len(self.chain) < 1:
            return
        caster = cmd.args['player_lifeform']
        target = cmd.args['interaction_target']
        return self.execute(caster, target)

    def execute(self, caster, target, **kwargs):
        mut_args = kwargs if kwargs else {}
        full_log = []
        for effect in self.chain:
            instance = effect()
            if not isinstance(instance, MagicEffect):
                continue
            log, mut_args = instance.enact(
                instigator=caster,
                target=SpellInstance.target(target, mut_args),
                **mut_args)
            if log:
                full_log.append(log)
        return full_log

    def target(target, mut_args):
        if not mut_args or 'target' not in mut_args:
            return target
        return mut_args['target']
