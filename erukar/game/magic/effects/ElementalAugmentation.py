from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ElementalAugmentation(SpellEffect):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0
    DamageName = ''
    DamageDescription = ''

    ParametersWhichShouldBeOverridden = []

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of acid damage to something, defaulting to the caster'''
        super().on_cast(command, lifeform, parameters)
        
        # Now to override
        for param in self.ParametersWhichShouldBeOverridden:
            if hasattr(self, param):
                parameters[param] = getattr(self, param)

        return parameters
