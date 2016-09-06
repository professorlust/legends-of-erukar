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

