from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Spear(Weapon):
    Probability = 1
    BaseName = "Spear"
    AttackRange = 1
    EssentialPart = "tip"

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.exponential
    DistributionProperties = (2,1)

    BaseStatInfluences = {
        'strength': {'requirement': 5, 'scaling_factor': 2.5, 'max_scale': 2},
        'dexterity':  {'requirement': 4, 'scaling_factor': 3.5, 'max_scale': 4}
    }