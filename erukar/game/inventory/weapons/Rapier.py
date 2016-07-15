from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Rapier(Weapon):
    Probability = 1
    BaseName = "Rapier"

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution (Note: Need to add ref to scipy for nonstandard)
    Distribution = np.random.normal
    DistributionProperties = (2, 0.3)
