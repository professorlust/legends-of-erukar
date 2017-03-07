from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
import random

class Cloaked(SpellWord):
    PotionName = 'Cloaking'
    PotionPriceMultiplier = 15.0
    ConditionType = 'Cloaked'

    ViewerResult = "{alias|target} becomes transparent!"
    TargetResult = "Your skin becomes transparent!"
    ParametersWhichShouldBeOverridden = ['ConditionType', 'ViewerResult', 'TargetResult']

