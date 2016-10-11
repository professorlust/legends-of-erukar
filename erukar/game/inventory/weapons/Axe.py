from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Axe(Weapon):
    Probability = 1
    BaseName = "Axe"
    EssentialPart = "edge"

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
        'strength': {'requirement': 5, 'scaling_factor': 2.5, 'max_scale': 4},
        'dexterity':  {'requirement': 0, 'scaling_factor': 3.5, 'max_scale': 3}
    }
