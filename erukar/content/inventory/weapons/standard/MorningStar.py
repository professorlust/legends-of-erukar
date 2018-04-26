from erukar.system.engine import Weapon
from ..categories.SimpleWeapon import SimpleWeapon
import numpy as np

class MorningStar(SimpleWeapon):
    Probability = 1
    BaseName = "Morning Star"
    EssentialPart = "head"
    BaseWeight = 10.9

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()

    BaseStatInfluences = {
        'strength': {'requirement': 7, 'scaling_factor': 4, 'cutoff': 200},
        'dexterity':  {'requirement': 0, 'scaling_factor': 1.25, 'cutoff': 200},
    }
