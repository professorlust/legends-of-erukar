from erukar.system.engine import EnergySource, SpellMutator


class BloodSource(EnergySource):
    EnergyToHealthRatio = 2.5
    Failed = 'You are too weak to draw enough blood for this spell!'
    ConsumeLife = 'You channel energy from your own blood, taking'\
        '{} damage in the process!'

    def source(self, caster, cmd, mutator):
        mutator.allocate_energy(caster)
        health_cost = int(self.EnergyToHealthRatio * mutator.allocated)
        if caster.health <= health_cost:
            cmd.append_result(caster.uid, self.Failed)
            return False, None

        caster.take_damage(health_cost, caster)
        mutator.confirm()
        cmd.log(caster, self.ConsumeLife.format(health_cost))
        return True, mutator or SpellMutator()
