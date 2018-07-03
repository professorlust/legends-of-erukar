from erukar.system.engine.inventory import FinesseWeapon
import numpy as np


class Claws(FinesseWeapon):
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
    CannotDrop = True
    AttackRange = 1
