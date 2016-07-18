from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Spear(Weapon):
    Probability = 1
    BaseName = "Spear"
    AttackRange = 1

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.exponential
    DistributionProperties = (2,1)
