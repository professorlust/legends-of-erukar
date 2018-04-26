from erukar.system.engine import Condition

class Wisened(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Wisened'
    Participle  = 'Wisening'
    Description = 'Increases Sense Score by 10'

    def modify_sense(self):
        return 10
