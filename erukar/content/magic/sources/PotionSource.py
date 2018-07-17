from erukar.system.engine import EnergySource, SpellMutator


class PotionSource(EnergySource):
    def source(self, caster, cmd, mutator):
        mutator = mutator or SpellMutator()
        mutator.allocated = 50
        mutator.confirm()
        return True, mutator
