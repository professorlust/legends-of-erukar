from erukar.system.engine import Transducer
import erukar


class InflictCondition(Transducer):
    SuccessSelf = 'You receive the {} condition temporarily.'
    SuccessTarget = '{} inflicts the {} condition on you!'
    SuccessInstigator = 'You inflict the {} condition on {}!'

    def transduce(self, instigator, target, cmd, mutator):
        condition = mutator.get('condition', erukar.Bolstered)
        condition(target, instigator)
        mutator.perform_mutation(condition)
        self.append_results(cmd, instigator, target, condition)
        return mutator

    def append_results(self, cmd, instigator, target, condition):
        if instigator is target:
            cmd.log(target, self.SuccessSelf.format(condition.Noun))
            return

        cmd.log(instigator, self.SuccessInstigator.format(
            target.alias(),
            condition.Noun
        ))
        cmd.log(target, self.SuccessTarget.format(
            instigator.alias(),
            condition.Noun
        ))
