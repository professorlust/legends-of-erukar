from erukar.engine.magic.MagicBase import MagicBase
from erukar.engine.model.Damage import Damage

class SpellWord(MagicBase):
    PotionName = 'Unintended Bug'
    PotionPriceMultiplier = 1.0

    ParametersWhichShouldBeOverridden = []
    RequiredSkill = None

    # Used with certain words, which can be ignored in the spell chain. Examples are TargetSelf, ArcaneSource, and TapAll
    Implied = False

    def on_cast(self, command, caster, parameters=None, efficacy=1.0):
        # Do nothing if we don't have the skill necessary to cast this
        if self.RequiredSkill is not None and not caster.get_skill(self.RequiredSkill) is None:
            return parameters
            
        super().on_cast(command, caster, parameters)
        
        # Now to override
        for param in self.ParametersWhichShouldBeOverridden:
            if hasattr(self, param):
                parameters[param] = getattr(self, param)

        return parameters
