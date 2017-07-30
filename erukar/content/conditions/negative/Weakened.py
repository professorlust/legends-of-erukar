from erukar.system.engine import Condition

class Weakened(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Weaken'
    Participle  = 'Weakening'
    Description = 'Lowers effective Strength Score by 50%'

    def modify_strength(self):
        return -self.target.strength/2
