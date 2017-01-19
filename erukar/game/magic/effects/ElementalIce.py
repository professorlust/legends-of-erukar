from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalIce(ElementalAugmentation):
    DamageName = 'ice'
    DamageDescription = "{alias|target} rapidly frosts over!"
    AugmentationType = 'Frost'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription', 'AugmentationType']

    PotionName = 'Ice'
    PotionPriceMultiplier = 3.5
