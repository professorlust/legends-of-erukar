from erukar.system.engine import Condition

class Vertigo(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Vertigo'
    Participle  = 'Inflicting Vertigo'
    Description = 'Lowers effective Dexterity Score by 50%'

    def modify_dexterity(self):
        return -self.target.dexterity/2
