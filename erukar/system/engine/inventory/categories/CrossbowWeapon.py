from .MartialWeapon import MartialWeapon
import numpy as np

class CrossbowWeapon(MartialWeapon):
    Variant = 'crossbow'
    RequiresAmmo          = True
    AmmoType              = 'Bolt'
    BludgeoningPercentage = 0.10
    SlashingPercentage    = 0.00
    PiercingPercentage    = 0.90
    DamageVariance        = 0.25
    ModifierPath = 'erukar.content.modifiers.ranged'
