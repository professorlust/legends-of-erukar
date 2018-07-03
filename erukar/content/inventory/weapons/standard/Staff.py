from erukar.system.engine.inventory import ArcaneWeapon
import numpy as np

class Staff(ArcaneWeapon):
    Probability = 1
    BaseName = "Staff"
    EssentialPart = "head"
    BaseWeight = 6.0

    # Damage
    DamageRange = [2, 6]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.uniform
    DistributionProperties = ()
    RequiresTwoHands = True

    BaseStatInfluences = {
        'acuity':  {'requirement': 6, 'scaling_factor': 3, 'cutoff': 200},
        'strength': {'requirement': 4, 'scaling_factor': 2, 'cutoff': 200},
    }
