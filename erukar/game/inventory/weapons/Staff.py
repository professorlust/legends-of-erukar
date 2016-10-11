from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Staff(Weapon):
    Probability = 1
    BaseName = "Staff"
    EssentialPart = "head"

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()

    BaseStatInfluences = {
        'acuity':  {'requirement': 6, 'scaling_factor': 3, 'max_scale': 3},
        'strength': {'requirement': 4, 'scaling_factor': 2, 'max_scale': 4}
    }
