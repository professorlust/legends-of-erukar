from ..categories.PolearmWeapon import PolearmWeapon
import numpy as np

class Spear(PolearmWeapon):
    Probability = 1
    BaseName = "Spear"
    AttackRange = 1
    EssentialPart = "tip"
    BaseWeight = 8.5

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.exponential
    DistributionProperties = (2,1)

    BaseStatInfluences = {
        'strength': {'requirement': 5, 'scaling_factor': 2.5, 'cutoff': 200},
        'dexterity':  {'requirement': 4, 'scaling_factor': 3.5, 'cutoff': 200},
    }
