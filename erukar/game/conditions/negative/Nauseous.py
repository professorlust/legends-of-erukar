from erukar.engine.model.Condition import Condition
import erukar

class Nauseous(Condition):
    IsTemporary = True
    Duration = 8 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    vitality = -10
