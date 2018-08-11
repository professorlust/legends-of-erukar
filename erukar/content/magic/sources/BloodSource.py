from erukar.system.engine import EnergySource, SpellMutator
import erukar


class BloodSource(EnergySource):
    EnergyToHealthRatio = 2.5
    NotSkilled = 'You do not possess the ability to use blood magic.'
    Failed = 'You are too weak to draw enough blood for this spell!'
    ConsumeLife = 'You channel energy from your own blood, taking'\
        '{} damage in the process!'

    def source(self, caster, cmd, mutator):
        if not caster.has_skill(erukar.BloodMagic):
            cmd.log(caster, self.NotSkilled)
            return False, None
        bloodmagic = caster.get_skill(erukar.BloodMagic)
        mutator.allocate_energy(caster)
        cost = mutator.allocated / bloodmagic.energy_created()
        if caster.health <= int(cost):
            cmd.append_result(caster.uid, self.Failed)
            return False, None
        caster.take_damage(cost, caster)
        mutator.confirm()
        cmd.log(caster, self.ConsumeLife.format(cost))
        return True, mutator or SpellMutator()
