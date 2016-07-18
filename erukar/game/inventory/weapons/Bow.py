from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Bow(Weapon):
    Probability = 1
    BaseName = "Bow"
    AttackRange = 3
    RangePenalty = 2

    # Damage
    DamageRange = [1, 5]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.gamma
    Shape = 2
    Scale = 0.25
    DistributionProperties = (Shape, Scale)

