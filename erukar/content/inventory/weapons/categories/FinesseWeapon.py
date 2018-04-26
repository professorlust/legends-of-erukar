from .MartialWeapon import MartialWeapon
import numpy as np

class FinesseWeapon(MartialWeapon):
    Variant = 'finesse'
    BludgeoningPercentage = 0.05
    SlashingPercentage    = 0.10
    PiercingPercentage    = 0.85
    DamageVariance        = 0.20
