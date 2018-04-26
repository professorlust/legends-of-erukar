from erukar.system.engine import Condition

class Bolstered(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Bolstered'
    Participle  = 'Bolstering'
    Description = 'Increases Strength Score by 10'

    def modify_strength(self):
        return 10
