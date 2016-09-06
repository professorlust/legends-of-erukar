from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Sword(Weapon):
    Probability = 100
    BaseName = "Sword"
    EssentialPart = "blade"

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.beta
    DistributionProperties = (2,2)

