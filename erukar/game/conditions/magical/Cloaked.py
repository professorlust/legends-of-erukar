from erukar.engine.model.Condition import Condition
import erukar

class Cloaked(Condition):
    Incapacitates = False
    BaseAcuityModifier = 20

    Noun        = 'Cloaked'
    Participle  = 'Cloaking'
    Description = 'Raises ATD (Acuity to Detect) by {}'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)

    def describe(self):
        return self.Description.format(self.modify_acuity_to_detect())

    def modify_acuity_to_detect(self):
        return int(self.BaseAcuityModifier * self.efficiency)
