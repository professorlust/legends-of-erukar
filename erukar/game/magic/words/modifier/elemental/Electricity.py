from erukar.game.magic.words.base.ElementalAugmentation import ElementalAugmentation
import random

class Electricity(ElementalAugmentation):
    DamageName = 'electricity'
    DamageDescription = 'Lightning strikes {alias|target} and electricity courses through his body!'
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'electric'

    PotionName = 'Electricity'
    PotionPriceMultiplier = 3.5
