from ..categories.SwordWeapon import SwordWeapon
import numpy as np

class BastardSword(SwordWeapon):
    MaximumRange = 1
    Probability = 2
    BaseName = "Bastard Sword"
    EssentialPart = "blade"
    BaseWeight = 7.0

    # Damage
    DamageRange = [3, 8]
    DamageType = "slashing"
    DamageModifier = "strength"

    # Distribution
    Distribution = np.random.beta
    DistributionProperties = (2,2)

    BaseStatInfluences = {
        'strength':  {'requirement': 4, 'scaling_factor': 5.0, 'cutoff': 200},
        'dexterity': {'requirement': 2, 'scaling_factor': 1.75, 'cutoff': 100},
    }

    RequiresTwoHands = True
