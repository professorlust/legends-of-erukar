from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDivine(ElementalAugmentation):
    DamageName = 'divine'
    DamageDescription = "Holy light pierces {alias|target}!"
    AugmentationType = 'Blessed'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription', 'AugmentationType']

    PotionName = 'Divine'
    PotionPriceMultiplier = 3.5
