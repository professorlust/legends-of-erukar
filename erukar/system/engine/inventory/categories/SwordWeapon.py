from .MartialWeapon import MartialWeapon
import numpy as np

class SwordWeapon(MartialWeapon):
    Variant = 'sword'
    BludgeoningPercentage = 0.10
    PiercingPercentage    = 0.10
    SlashingPercentage    = 0.80
