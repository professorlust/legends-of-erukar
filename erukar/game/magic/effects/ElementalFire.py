from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalFire(ElementalAugmentation):
    DamageName = 'fire'
    DamageDescription = "Flames engulf {alias|target}'s body!"
    AugmentationType = 'Flaming'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription', 'AugmentationType']

    PotionName = 'Fire'
    PotionPriceMultiplier = 3.5
