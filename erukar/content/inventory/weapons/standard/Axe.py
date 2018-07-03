from erukar.system.engine.inventory import AxeWeapon
import numpy as np


class Axe(AxeWeapon):
    Probability = 1
    BaseName = "Axe"
    EssentialPart = "edge"
    BaseWeight = 4.0

    # Damage
    DamageRange = [4, 8]

    # Distribution
    Distribution = np.random.exponential
    Scale = 2
    Size = 1
    DistributionProperties = (Scale, Size)

    BaseStatInfluences = {
        'strength': {'requirement': 5, 'scaling_factor': 3.5, 'cutoff': 200},
        'dexterity':  {'requirement': 0, 'scaling_factor': 1.5, 'cutoff': 200},
    }
