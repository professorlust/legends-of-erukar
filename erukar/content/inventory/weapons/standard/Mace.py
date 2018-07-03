from erukar.system.engine.inventory import SimpleWeapon
import numpy as np

class Mace(SimpleWeapon):
    Probability = 1
    BaseName = "Mace"
    EssentialPart = "head"
    BaseWeight = 10.0

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()
