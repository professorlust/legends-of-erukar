from erukar.engine.model.Condition import Condition
import erukar

class Undead(Condition):
    Incapacitates = False
    IsTemporary = False
    DamageMitigations = {
        'divine': (-0.5, 0),
        'demonic': (0.25, 0)
    }
