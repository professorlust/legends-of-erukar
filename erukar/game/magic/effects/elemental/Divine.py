from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDivine(ElementalAugmentation):
    DamageName = 'divine'
    DamageDescription = "{alias|target} is consumed by divine light!"
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'divine'

    PotionName = 'Divine'
    PotionPriceMultiplier = 3.5
