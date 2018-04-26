from .MartialWeapon import MartialWeapon
import numpy as np

class PolearmWeapon(MartialWeapon):
    Variant = 'polearm'
    RequiresTwoHands      = True
    BludgeoningPercentage = 0.20
    SlashingPercentage    = 0.40
    PiercingPercentage    = 0.40
    DamageVariance        = 0.75
