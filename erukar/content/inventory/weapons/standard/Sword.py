from erukar.system.engine import Weapon
import numpy as np

class Sword(Weapon):
    Probability = 2
    BaseName = "Sword"
    EssentialPart = "blade"
    BaseWeight = 7.0

    # Damage
    DamageRange = [2, 6]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.beta
    DistributionProperties = (2,2)

    BaseStatInfluences = {
        'strength':  {'requirement': 4, 'scaling_factor': 4, 'cutoff': 200},
        'dexterity': {'requirement': 3, 'scaling_factor': 3, 'cutoff': 200},
    }
