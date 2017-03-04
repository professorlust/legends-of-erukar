from erukar.game.magic.words.basic.ElementalAugmentation import ElementalAugmentation
import random

class Fire(ElementalAugmentation):
    DamageName = 'fire'
    DamageDescription = "Flames engulf {alias|target}'s body!"
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'fire'

    PotionName = 'Fire'
    PotionPriceMultiplier = 3.5
