from erukar.engine.model.SpellEffect import SpellEffect

class ArcaneAdeptAugmentation(SpellEffect):
    DamageShouldScale = True
    DamageScalar = 3

    ParametersWhichShouldBeOverridden = ['DamageShouldScale', 'DamageScalar']

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        super().on_cast(command, lifeform, parameters)
        
        # Now to override
        for param in self.ParametersWhichShouldBeOverridden:
            if hasattr(self, param):
                parameters[param] = getattr(self, param)

        return parameters
