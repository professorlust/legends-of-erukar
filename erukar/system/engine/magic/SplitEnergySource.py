from .EnergySource import EnergySource


class SplitEnergySource(EnergySource):
    '''
    This is a unique Energy Source which is used with Selectors and
    Splitters. It should not be used in a spell chain, as it is
    automatically generated..
    '''
    def source(self, caster, cmd, mutator):
        return True, mutator
