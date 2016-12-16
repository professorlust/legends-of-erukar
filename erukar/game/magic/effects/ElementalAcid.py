from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalAcid(ElementalAugmentation):
    DamageName = 'acid'
    DamageDescription = 'Acid engulfs {alias|target}\'s body!'

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']
