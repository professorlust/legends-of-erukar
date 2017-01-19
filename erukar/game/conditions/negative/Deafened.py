from erukar.engine.model.Condition import Condition
import erukar

class Deafened(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def modify_acuity(self):
        return -self.target.sense
