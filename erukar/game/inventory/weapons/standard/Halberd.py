from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Halberd(Weapon):
    Probability = 1
    BaseName = "Halberd"
    EssentialPart = "head"
    AttackRange = 1
    BaseWeight = 13.5

    # Damage
    DamageRange = [3, 6]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.exponential
    Scale = 2
    Size = 1
    DistributionProperties = (Scale, Size)

    BaseStatInfluences = {
        'strength': {'requirement': 4, 'scaling_factor': 3.5, 'max_scale': 4},
        'dexterity':  {'requirement': 5, 'scaling_factor': 2.5, 'max_scale': 2}
    }
