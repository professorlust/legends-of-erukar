from erukar.system.engine import Weapon
import numpy as np

class Claws(Weapon):
    IsInteractible = False
    Probability = 0
    BaseName = "Claws"
    EssentialPart = "points"

    # Damage
    DamageRange = [1, 5]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()
