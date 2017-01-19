from erukar.engine.model.SpellEffect import SpellEffect
from erukar.engine.model.Damage import Damage
import random

class ElementalAugmentation(SpellEffect):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0
    DamageName = ''
    DamageDescription = ''

    PotionName = 'Elemental'
    PotionPriceMultiplier = 3.0
