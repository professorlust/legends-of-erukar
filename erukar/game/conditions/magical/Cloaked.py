from erukar.engine.model.Condition import Condition
import erukar

class Cloaked(Condition):
    Incapacitates = False
    BaseAcuityModifier = 20

    Noun        = 'Cloaked'
    Participle  = 'Cloaking'
    Description = 'Raises the necessary acuity to be visually detected by 20'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)

    def modify_acuity_to_detect(self):
        return self.BaseAcuityModifier * self.efficiency
