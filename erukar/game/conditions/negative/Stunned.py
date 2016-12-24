from erukar.engine.model.Condition import Condition
import erukar

class Stunned(Condition):
    IsTemporary = True
    Duration = 2 # In ticks, where a tick is 5 seconds
    Incapacitates = True

