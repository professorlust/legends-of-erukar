from erukar.system.engine import EnergySource, SpellMutator


class ArcaneEnergySource(EnergySource):
    def source(self, caster, cmd, mutator):
        mutator.allocate_energy(caster)
        if mutator.allocated > caster.arcane_energy:
            cmd.append_result(caster.uid, self.Failed)
            return False, None

        caster.arcane_energy -= mutator.allocated
        mutator.confirm()
        return True, mutator or SpellMutator()
