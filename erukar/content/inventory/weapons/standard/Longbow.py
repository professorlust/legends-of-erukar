from erukar.system.engine import Weapon
import numpy as np

class Longbow(Weapon):
    Probability = 1
    BaseName = "Longbow"
    EssentialPart = "bowstrings"
    BaseWeight = 2.0
    AttackRange = 7
    RangePenalty = 3

    # Damage
    DamageRange = [1, 5]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.gamma
    Shape = 2
    Scale = 0.25
    DistributionProperties = (Shape, Scale)

    RequiresTwoHands = True
    RequiresAmmo     = True
    AmmoType         = 'Arrow'

    BaseStatInfluences = {
        'dexterity':  {'requirement': 8, 'scaling_factor': 3, 'cutoff': 200},
    }

    Variant = 'bow'
