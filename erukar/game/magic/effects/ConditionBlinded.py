from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ConditionBlinded(SpellEffect):
    PotionName = 'Blinding'
    PotionPriceMultiplier = 3.0
    ConditionType = 'Blinded'

    ParametersWhichShouldBeOverridden = ['ConditionType']

