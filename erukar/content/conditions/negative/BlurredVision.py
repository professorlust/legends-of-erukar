from erukar.system.engine import Condition

class BlurredVision(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    
    Noun        = 'Blurry Vision'
    Participle  = 'Blurring Vision'
    Description = 'Halves effective Acuity score'

    def modify_acuity(self):
        return -int(self.target.acuity/2)

