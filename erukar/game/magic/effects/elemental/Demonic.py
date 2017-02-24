from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDemonic(ElementalAugmentation):
    DamageName = 'demonic'
    DamageDescription = "{alias|target} is swallowed by demonic darkness!"
    AugmentationType = 'AdditionalDamage'
    AugmentationSubclass = 'demonic'

    PotionName = 'Demonic'
    PotionPriceMultiplier = 3.5
