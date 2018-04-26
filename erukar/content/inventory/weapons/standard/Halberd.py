from ..categories.PolearmWeapon import PolearmWeapon
import numpy as np

class Halberd(PolearmWeapon):
    Probability = 1
    BaseName = "Halberd"
    EssentialPart = "head"
    AttackRange = 2
    BaseWeight = 13.5

    # Damage
    DamageRange = [3, 7]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.exponential
    Scale = 2
    Size = 1
    DistributionProperties = (Scale, Size)

    RequiresTwoHands = True
    BaseStatInfluences = {
        'strength': {'requirement': 4, 'scaling_factor': 3.5, 'cutoff': 200},
        'dexterity':  {'requirement': 5, 'scaling_factor': 2.5, 'cutoff': 200},
    }
