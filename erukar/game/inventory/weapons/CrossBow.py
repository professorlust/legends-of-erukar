from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class CrossBow(Weapon):
    Probability = 1
    BaseName = "CrossBow"
    AttackRange = 2
    RangePenalty = 2

    # Damage
    DamageRange = [1, 4]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.gamma
    Shape = 2
    Scale = 0.25
    DistributionProperties = (Shape, Scale)

