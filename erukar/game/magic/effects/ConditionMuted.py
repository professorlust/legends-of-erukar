from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ConditionMuted(SpellEffect):
    PotionName = 'Muting'
    PotionPriceMultiplier = 15.0
    ConditionType = 'Muted'

    ViewerResult = "All of {alias|target}'s sounds become hushed!"
    TargetResult = "Your sounds become muted!"
    ParametersWhichShouldBeOverridden = ['ConditionType', 'ViewerResult', 'TargetResult']
