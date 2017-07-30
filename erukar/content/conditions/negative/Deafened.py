from erukar.system.engine import Condition

class Deafened(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Deafness'
    Participle  = 'Deafening'
    Description = 'Reduces effective Sense score to zero'

    def modify_sense(self):
        return -self.target.sense
