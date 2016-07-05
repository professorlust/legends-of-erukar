from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Bow(Weapon):
    Probability = 100
    BaseName = "Bow"

    # Damage
    DamageRange = (1, 5)
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.gamma
    Shape = 2
    Scale = 2
    Size = 2
    DistributionProperties = (Shape, Scale, Size)

