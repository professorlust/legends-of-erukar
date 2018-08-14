from erukar.system.engine import MagicEffect


class Selector(MagicEffect):
    '''
    A Selector is an optional piece of a spell chain which can make
    the spell affect multiple targets.
    '''
    def evasion(self, caster, target, cmd, mutator):
        return None

    def applicable_targets(self, caster, cmd, mutator):
        yield mutator.get('target')

    def adjust_energy(self, num_targets, mutator):
        mutator.energy /= max(1, num_targets)
