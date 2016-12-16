from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalDemonic(ElementalAugmentation):
    DamageName = 'divine'
    DamageDescription = "{alias|target} is swallowed by demonic darkness!"

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']
