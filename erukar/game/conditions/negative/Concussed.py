from erukar.engine.model.Condition import Condition
import erukar

class Concussed(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def modify_acuity(self):
        return -self.target.sense/2

    Noun        = 'Concussion'
    Participle  = 'Concussing'
    Description = 'Halves effective Sense score'
