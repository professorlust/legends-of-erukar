from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalIce(ElementalAugmentation):
    DamageName = 'ice'
    DamageDescription = "{alias|target} rapidly frosts over!"

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']

    PotionName = 'Ice'
    PotionPriceMultiplier = 3.5
