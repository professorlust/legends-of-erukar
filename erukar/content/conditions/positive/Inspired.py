from erukar.system.engine import Condition

class Inspired(Condition):
    IsTemporary = True
    Duration = 30 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Inspiration'
    Participle  = 'Inspiring'
    Description = 'Increases Resolve Score by 10'

    def modify_resolve(self):
        return 10
