from erukar.system.engine import Condition

class Stunned(Condition):
    IsTemporary = True
    Duration = 2 # In ticks, where a tick is 5 seconds
    Incapacitates = True

    Noun        = 'Stun'
    Participle  = 'Stunning'
    Description = 'Incapacitates completely for a duration'
