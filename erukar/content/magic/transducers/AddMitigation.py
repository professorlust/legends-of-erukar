from erukar.system.engine import Transducer
import erukar


class AddMitigation(Transducer):
    DefaultType = 'fire'
    DefaultPower = 1.25
    Success = 'You receive an additional {}% {} mitigation!'

    def transduce(self, instigator, target, cmd, mutator):
        damage_type = mutator.get('damage_type', self.DefaultType)
        power = mutator.power()
        percent = AddMitigation.percentage(power)
        condition_type = erukar.content.conditions.BonusMitigation
        condition = condition_type(target, instigator)
        condition.mitigation_amount = percent
        condition.damage_type = damage_type
        cmd.log(instigator, self.Success.format(int(percent*100), damage_type))
        return mutator

    def percentage(power):
        return 0.04 * power
