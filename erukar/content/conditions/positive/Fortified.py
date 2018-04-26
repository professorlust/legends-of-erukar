from erukar.system.engine import Condition

class Fortified(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Fortified'
    Participle  = 'Fortifying'
    Description = 'Increases Vitality Score by 10'

    def modify_vitality(self):
        return 10
