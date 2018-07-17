from erukar.system.engine import MagicEffect


class Transducer(MagicEffect):
    '''
    A Transducer Effect is one that takes all modifications in
    the spell chain and turns them into something, be that damage,
    conditions, or healing.
    '''
    EnergyPercentageConsumed = 0.75

    def enact(self, instigator, target, cmd, mutator):
        self.transduce(instigator, target, cmd, mutator)
        mutator.energy *= self.EnergyPercentageConsumed
        return mutator

    def transduce(self, instigator, target, cmd, **kwargs):
        return kwargs
