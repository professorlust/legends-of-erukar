from erukar.system.engine import Condition

class Ethereal(Condition):
    Incapacitates = False
    IsTemporary = False
    DamageMitigations = {
        'bludgeoning': (0.333, 0),
        'piercing': (0.333, 0),
        'slashing': (0.333, 0)
    }

    Noun        = 'Ethereal'
    Participle  = 'Being Ethereal'
    Description = 'Partial transition into Ethereal Plane, reducing physical damage by 33%'
