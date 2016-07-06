from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Halberd(Weapon):
    Probability = 1
    BaseName = "Halberd"

    # Damage
    DamageRange = [3, 6]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.exponential
    Scale = 2
    Size = 1 
    DistributionProperties = (Scale, Size)

