from erukar.engine.model.Condition import Condition
import erukar

class Blinded(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Blindness'
    Participle  = 'Blinding'
    Description = 'Reduces Acuity to Zero'

    def modify_acuity(self):
        return -self.target.acuity
