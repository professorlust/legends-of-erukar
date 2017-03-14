from erukar.game.magic.words.base.ElementalAugmentation import ElementalAugmentation
import random

class Ice(ElementalAugmentation):
    DamageName = 'ice'
    DamageDescription = "{alias|target} rapidly frosts over!"
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'ice'

    PotionName = 'Ice'
    PotionPriceMultiplier = 3.5
