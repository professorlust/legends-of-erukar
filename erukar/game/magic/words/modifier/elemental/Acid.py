from erukar.game.magic.words.base.ElementalAugmentation import ElementalAugmentation
import random

class Acid(ElementalAugmentation):
    DamageName = 'acid'
    DamageDescription = 'Acid engulfs {alias|target}\'s body!'
    AugmentationType = 'AdditionalDamage'
    augmentationSubclass = 'Acid'

    PotionName = 'Acid'
    PotionPriceMultiplier = 3.5
