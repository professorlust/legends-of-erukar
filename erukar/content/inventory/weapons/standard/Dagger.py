from erukar.system.engine import Weapon
from ..categories.FinesseWeapon import FinesseWeapon
import numpy as np

class Dagger(FinesseWeapon):
    Probability = 1
    BaseName = "Dagger"
    EssentialPart = "blade"
    BaseWeight = 1.75

    # Damage
    DamageRange = [1, 4]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution (Note: Need to add ref to scipy for nonstandard)
    Distribution = np.random.normal
    DistributionProperties = (2, 0.3)

    BaseStatInfluences = {
        'dexterity':  {'requirement': 4, 'scaling_factor': 6, 'cutoff': 220},
    }
