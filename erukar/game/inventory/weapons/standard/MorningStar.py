from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class MorningStar(Weapon):
    Probability = 1
    BaseName = "Morning Star"
    EssentialPart = "head"
    BaseWeight = 10.9

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()

    BaseStatInfluences = {
        'strength': {'requirement': 7, 'scaling_factor': 4, 'max_scale': 6},
        'dexterity':  {'requirement': 0, 'scaling_factor': 1.25, 'max_scale': 2}
    }
