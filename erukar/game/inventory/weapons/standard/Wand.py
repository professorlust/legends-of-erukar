from erukar.engine.inventory.Weapon import Weapon
import numpy as np
import random

class Wand(Weapon):
    Probability = 1
    BaseName = "Wand"
    EssentialPart = "tip"
    AttackRange = 2
    RangePenalty = 2
    BaseWeight = 1.0

    # Damage
    DamageRange = [2, 6]
    DamageType = 'force'
    DamageModifier = "acuity"

    # Distribution
    Distribution = np.random.gamma
    DistributionProperties = (2, 0.3)

    BaseStatInfluences = {
        'acuity':  {'requirement': 8, 'scaling_factor': 3, 'cutoff': 200},
        'dexterity': {'requirement': 0, 'scaling_factor': 1.5, 'cutoff': 200},
    }
