from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
import random

class Enraged(SpellWord):
    PotionName = 'Rage'
    PotionPriceMultiplier = 16.0
    ConditionType = 'Enraged'

    ParametersWhichShouldBeOverridden = ['ConditionType']
    RequiredSkill = 'erukar.game.skills.brutality.Rage'
