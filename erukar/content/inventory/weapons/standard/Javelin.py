from erukar.system.engine import Weapon
import numpy as np

class Javelin(Weapon):
    Probability = 1
    BaseName = "Javelin"
    AttackRange = 2
    EssentialPart = "head"
    BaseWeight = 8.5

    # Damage
    DamageRange = [2, 4]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.exponential
    DistributionProperties = (2,1)

    BaseStatInfluences = {
        'strength': {'requirement': 5, 'scaling_factor': 2.5, 'cutoff': 200},
        'dexterity':  {'requirement': 4, 'scaling_factor': 3.5, 'cutoff': 200},
    }

    Variant = 'polearm'
