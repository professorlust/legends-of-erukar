from erukar.engine.model.Condition import Condition
import erukar

class Nauseous(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Nausea'
    Participle  = 'Nauesating'
    Description = 'Lowers effective Vitality Score by 50%'

    def modify_vitality(self):
        return -self.target.sense/2
