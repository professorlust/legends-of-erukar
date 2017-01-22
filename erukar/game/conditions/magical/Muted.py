from erukar.engine.model.Condition import Condition
import erukar

class Muted(Condition):
    Incapacitates = False
    BaseSenseModifier = 20

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.efficacy = 1.0

    def modify_acuity_to_detect(self):
        return self.BaseSenseModifier * self.efficiency
