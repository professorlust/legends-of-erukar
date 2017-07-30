from erukar.system.engine import Condition

class Disoriented(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def modify_acuity(self):
        return -int(self.target.acuity/4)
    
    def modify_sense(self):
        return -int(self.target.sense/4)

    Noun        = 'Disorientation'
    Participle  = 'Disorienting'
    Description = 'Reduces effective Acuity and Sense scores by 25%'
