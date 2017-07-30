from erukar.system.engine import Condition

class Terrified(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Terror'
    Participle  = 'Terrifying'
    Description = 'Lowers effective Resolve Score by 50%'

    def modify_resolve(self):
        return -self.target.resolve/2
