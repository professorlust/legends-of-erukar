from erukar.game.magic.effects.ElementalAugmentation import ElementalAugmentation
import random

class ElementalFire(ElementalAugmentation):
    DamageName = 'fire'
    DamageDescription = "Flames engulf {alias|target}'s body!"

    ParametersWhichShouldBeOverridden = ['DamageName','DamageDescription']
