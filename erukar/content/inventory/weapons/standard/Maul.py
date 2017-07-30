from erukar.system.engine import Weapon
import numpy as np

class Maul(Weapon):
    Probability = 1
    BaseName = "Maul"
    EssentialPart = "head"
    BaseWeight = 11.5

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()

    BaseStatInfluences = {
        'strength': {'requirement': 3, 'scaling_factor': 5, 'cutoff': 200},
        'dexterity':  {'requirement': 0, 'scaling_factor': 1.25, 'cutoff': 200},
    }
