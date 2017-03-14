from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
import random

class Muted(SpellWord):
    PotionName = 'Muting'
    PotionPriceMultiplier = 15.0
    ConditionType = 'Muted'

    ViewerResult = "All of {alias|target}'s sounds become hushed!"
    TargetResult = "Your sounds become muted!"
    ParametersWhichShouldBeOverridden = ['ConditionType', 'ViewerResult', 'TargetResult']
