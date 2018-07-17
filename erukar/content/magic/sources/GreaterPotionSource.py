from erukar.system.engine import EnergySource, SpellMutator


class GreaterPotionSource(EnergySource):
    def source(self, caster, cmd, mutator):
        mutator = mutator or SpellMutator()
        mutator.allocated = 100
        mutator.confirm()
        return True, mutator
