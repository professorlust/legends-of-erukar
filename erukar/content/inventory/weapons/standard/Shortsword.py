from erukar.system.engine.inventory import SwordWeapon
import numpy as np

class Shortsword(SwordWeapon):
    MaximumRange = 1
    Probability = 2
    BaseName = "Shortsword"
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
