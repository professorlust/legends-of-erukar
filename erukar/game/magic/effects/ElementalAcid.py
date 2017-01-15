from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalAcid(ElementalAugmentation):
    DamageName = 'acid'
    DamageDescription = 'Acid engulfs {alias|target}\'s body!'

    PotionName = 'Acid'
    PotionPriceMultiplier = 3.5

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']
