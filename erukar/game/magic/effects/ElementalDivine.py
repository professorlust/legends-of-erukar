from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDivine(ElementalAugmentation):
    DamageName = 'divine'
    DamageDescription = "Holy light pierces {alias|target}!"

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']

    PotionName = 'Divine'
    PotionPriceMultiplier = 3.5
