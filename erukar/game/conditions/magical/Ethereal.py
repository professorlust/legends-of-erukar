from erukar.engine.model.Condition import Condition
import erukar

class Ethereal(Condition):
    Incapacitates = False
    IsTemporary = False
    DamageMitigations = {
        'bludgeoning': (0.333, 0),
        'piercing': (0.333, 0),
        'slashing': (0.333, 0)
    }