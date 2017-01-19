from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDemonic(ElementalAugmentation):
    DamageName = 'demonic'
    DamageDescription = "{alias|target} is swallowed by demonic darkness!"
    AugmentationType = 'Cursed'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription', 'AugmentationType']

    PotionName = 'Demonic'
    PotionPriceMultiplier = 3.5
