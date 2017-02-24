from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ConditionCloaked(SpellEffect):
    PotionName = 'Cloaking'
    PotionPriceMultiplier = 15.0
    ConditionType = 'Cloaked'

    ViewerResult = "{alias|target} becomes transparent!"
    TargetResult = "Your skin becomes transparent!"
    ParametersWhichShouldBeOverridden = ['ConditionType', 'ViewerResult', 'TargetResult']

