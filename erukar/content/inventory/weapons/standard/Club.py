from erukar.system.engine.inventory import SimpleWeapon
import numpy as np

class Club(SimpleWeapon):
    Probability = 1
    BaseName = "Club"
    EssentialPart = "head"
    BaseWeight = 8.0
    MaximumRange = 1

    # Damage
    DamageRange = [1, 8]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()
