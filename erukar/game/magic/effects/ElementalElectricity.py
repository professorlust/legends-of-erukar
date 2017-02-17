from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalElectricity(ElementalAugmentation):
    DamageName = 'electricity'
    DamageDescription = 'Lightning strikes {alias|target} and electricity courses through his body!'
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'electric'

    PotionName = 'Electricity'
    PotionPriceMultiplier = 3.5
