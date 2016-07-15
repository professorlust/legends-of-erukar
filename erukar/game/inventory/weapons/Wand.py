from erukar.engine.inventory.Weapon import Weapon
import numpy as np
import random

class Wand(Weapon):
    Probability = 1
    BaseName = "Wand"

    # Damage
    DamageRange = [2, 6]
    DamageType = random.choice(['fire','acid','cold','electric']) 
    DamageModifier = "acuity"

    # Distribution
    Distribution = np.random.gamma
    DistributionProperties = (2, 0.3)
