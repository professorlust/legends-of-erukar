from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalIce(ElementalAugmentation):
    DamageName = 'ice'
    DamageDescription = "{alias|target} rapidly frosts over!"
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'ice'

    PotionName = 'Ice'
    PotionPriceMultiplier = 3.5
