from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ConditionEnraged(SpellEffect):
    PotionName = 'Rage'
    PotionPriceMultiplier = 16.0
    ConditionType = 'Enraged'

    ParametersWhichShouldBeOverridden = ['ConditionType']