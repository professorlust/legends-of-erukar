from .MartialWeapon import MartialWeapon
import numpy as np

class SimpleWeapon(MartialWeapon):
    Variant = 'simple'
    BludgeoningPercentage = 1.00
    SlashingPercentage    = 0.00
    PiercingPercentage    = 0.00
    DamageVariance        = 0.30
