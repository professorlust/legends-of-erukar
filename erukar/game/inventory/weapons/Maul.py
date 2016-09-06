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
