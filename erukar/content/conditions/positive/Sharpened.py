from erukar.system.engine import Condition

class Sharpened(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Sharpened'
    Participle  = 'Sharpening'
    Description = 'Increases Acuity Score by 10'

    def modify_sense(self):
        return 10
