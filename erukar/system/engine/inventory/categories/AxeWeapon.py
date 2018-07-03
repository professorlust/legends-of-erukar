from .MartialWeapon import MartialWeapon
import numpy as np

class AxeWeapon(MartialWeapon):
    Variant = 'axe'
    BludgeoningPercentage = 0.30
    SlashingPercentage    = 0.55
    PiercingPercentage    = 0.15
    DamageVariance        = 0.75
