from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
import random

class Frozen(SpellWord):
    PotionName = 'Freezing'
    PotionPriceMultiplier = 3.0
    ConditionType = 'Frozen'

    ViewerResult = "{alias|target} rapidly frosts over and stops moving!"
    TargetResult = "You experience a rapid freeze, chilling you down to the bone and preventing you from moving!"
    ParametersWhichShouldBeOverridden = ['ConditionType', 'ViewerResult', 'TargetResult']
