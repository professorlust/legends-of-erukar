from ..categories.AxeWeapon import AxeWeapon
import numpy as np

class Battleaxe(AxeWeapon):
    Probability = 1
    BaseName = "Battle Axe"
    EssentialPart = "edge"
    BaseWeight = 4.0

    # Damage
    DamageRange = [4, 8]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.exponential
    Scale = 2
    Size = 1
    DistributionProperties = (Scale, Size)

    BaseStatInfluences = {
        'strength': {'requirement': 5, 'scaling_factor': 2.5, 'cutoff': 200},
        'dexterity':  {'requirement': 0, 'scaling_factor': 3.5, 'cutoff': 200},
    }

    RequiresTwoHands = True
