from erukar.engine.model.Condition import Condition
import erukar

class BlurredVision(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def modify_acuity(self):
        return -int(self.target.acuity/2)

