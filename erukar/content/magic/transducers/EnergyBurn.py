from erukar.system.engine import Transducer, Lifeform, Attack


class EnergyBurn(Transducer):
    Success = 'You inflict {} damage on {}, burning {} energy!'
    TargetSuccess = '{} burns {} of your arcane energy, dealing {} damage to you!'
    Failed = 'Energy Burn failed!'

    def transduce(self, instigator, target, cmd, mutator):
        percent = EnergyBurn.percent(mutator.power())
        damage_type = mutator.get('damage_type', 'arcane')
        actual_energy = self.actual_energy(target, percent)
        if actual_energy <= 0:
            cmd.log(instigator, self.Failed)
            return mutator
        burn = int(actual_energy * EnergyBurn.damage_scalar(mutator.power()))
        target.arcane_energy -= actual_energy
        result = target.apply_damage(instigator, None, {
            damage_type: burn
        })
        damage_str = Attack.final_damages(result)
        log = self.Success.format(damage_str, target.alias(), actual_energy)
        target_str = self.TargetSuccess.format(
            instigator.alias(),
            damage_str,
            actual_energy)
        cmd.log(instigator, log)
        cmd.log(target, target_str)
        return mutator

    def percent(power):
        return 0.02 * power

    def damage_scalar(power):
        return 2 + 0.5 * power

    def actual_energy(self, target, percent):
        if not isinstance(target, Lifeform):
            return 0
        max_amount = int(max(0.0, target.maximum_arcane_energy() * percent))
        return target.arcane_energy\
            if max_amount > target.arcane_energy\
            else max_amount
