from erukar.system.engine.inventory import FinesseWeapon
import numpy as np


class Rapier(FinesseWeapon):
    Probability = 1
    BaseName = "Rapier"
    EssentialPart = "blade"
    BaseWeight = 4.5

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution (Note: Need to add ref to scipy for nonstandard)
    Distribution = np.random.normal
    DistributionProperties = (2, 0.3)

    BaseStatInfluences = {
        'strength': {'requirement': 2, 'scaling_factor': 1.5, 'cutoff': 200},
        'dexterity':  {'requirement': 8, 'scaling_factor': 5, 'cutoff': 200},
    }
