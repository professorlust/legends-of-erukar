from erukar.engine.model.Condition import Condition
import erukar

class Frozen(Condition):
    IsTemporary = True
    Duration = 1 # In ticks, where a tick is 5 seconds
    Incapacitates = True
    DamageMitigations = {
        'bludgeoning': (-0.3, 0),
        'piercing': (0.75, 0),
        'slashing': (0.75, 0),
        'ice': (1, 0),
        'fire': (1, 0),
    }

    Noun        = 'Frozen'
    Participle  = 'Freezing'
    Description = 'Stops target for a full turn, providing increased piercing, slashing, ice, and fire damage mitigation but highly reduced bludgeoning mitigation'
