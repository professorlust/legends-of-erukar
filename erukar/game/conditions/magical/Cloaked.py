from erukar.engine.model.Condition import Condition
import erukar

class Cloaked(Condition):
    Incapacitates = False

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)

    def tick(self):
        pass