from erukar.system.engine import Transducer
import erukar


class AddDeflection(Transducer):
    DefaultType = 'fire'
    Success = 'You receive {} additional {} deflection!'

    def transduce(self, instigator, target, cmd, mutator):
        damage_type = mutator.get('damage_type', self.DefaultType)
        amount = AddDeflection.amount(mutator.power())
        condition_type = erukar.content.conditions.BonusDeflection
        condition = condition_type(target, instigator)
        condition.deflection_amount = amount
        condition.damage_type = damage_type
        cmd.log(target, self.Success.format(amount, damage_type))
        return mutator

    def amount(power):
        return int(power * 2)
