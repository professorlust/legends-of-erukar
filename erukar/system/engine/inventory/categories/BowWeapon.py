from .MartialWeapon import MartialWeapon
import numpy as np

class BowWeapon(MartialWeapon):
    Variant = 'bow'
    RequiresTwoHands      = True
    RequiresAmmo          = True
    AmmoType              = 'Arrow'
    BludgeoningPercentage = 0.10
    SlashingPercentage    = 0.00
    PiercingPercentage    = 0.90
    DamageVariance        = 0.50
    ModifierPath = 'erukar.content.modifiers.ranged'
