from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Maul(Weapon):
    Probability = 1
    BaseName = "Maul"
    EssentialPart = "head"

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()

    BaseStatInfluences = {
        'strength': {'requirement': 3, 'scaling_factor': 5, 'max_scale': 4},
        'dexterity':  {'requirement': 0, 'scaling_factor': 1.25, 'max_scale': 2}
    }
