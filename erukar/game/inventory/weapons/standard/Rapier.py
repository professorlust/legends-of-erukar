from erukar.engine.inventory.Weapon import Weapon
import numpy as np

class Rapier(Weapon):
    Probability = 1
    BaseName = "Rapier"
    EssentialPart = "blade"
    BaseWeight = 4.5

    # Damage
    DamageRange = [2, 6]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution (Note: Need to add ref to scipy for nonstandard)
    Distribution = np.random.normal
    DistributionProperties = (2, 0.3)

    BaseStatInfluences = {
        'strength': {'requirement': 2, 'scaling_factor': 1.5, 'max_scale': 2},
        'dexterity':  {'requirement': 8, 'scaling_factor': 5, 'max_scale': 6}
    }
