from erukar.system.engine import Condition

class Graceful(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Graceful'
    Participle  = 'Gracing'
    Description = 'Increases Dexterity Score by 10'

    def modify_dexterity(self):
        return 10
