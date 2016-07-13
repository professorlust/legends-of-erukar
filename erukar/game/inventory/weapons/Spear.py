from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Spear(Weapon):
    Probability = 1
    BaseName = "Spear"

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()
