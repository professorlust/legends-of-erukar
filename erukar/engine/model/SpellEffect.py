from erukar.engine.model.MagicBase import MagicBase
from erukar.engine.model.Damage import Damage

class SpellEffect(MagicBase):
    PotionName = 'Unintended Bug'
    PotionPriceMultiplier = 1.0

    ParametersWhichShouldBeOverridden = []

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        super().on_cast(command, lifeform, parameters)
        
        # Now to override
        for param in self.ParametersWhichShouldBeOverridden:
            if hasattr(self, param):
                parameters[param] = getattr(self, param)

        return parameters
