from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
import random

class Blinded(SpellWord):
    PotionName = 'Blinding'
    PotionPriceMultiplier = 3.0
    ConditionType = 'Blinded'

    ParametersWhichShouldBeOverridden = ['ConditionType']

