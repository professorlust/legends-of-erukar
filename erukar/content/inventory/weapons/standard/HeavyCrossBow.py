from erukar.system.engine import Weapon
import numpy as np

class HeavyCrossBow(Weapon):
    Probability = 1
    BaseName = "Heavy Crossbow"
    EssentialPart = "string"
    BaseWeight = 5.5
    AttackRange = 6
    RangePenalty = 3

    # Damage
    DamageRange = [2, 8]
    DamageType = "piercing"
    DamageModifier = "dexterity"

    # Distribution
    Distribution = np.random.gamma
    Shape = 2
    Scale = 0.25
    DistributionProperties = (Shape, Scale)

    RequiresAmmo = True
    AmmoType     = 'CrossbowBolt'

    BaseStatInfluences = {
        'dexterity':  {'requirement': 6, 'scaling_factor': 5, 'cutoff': 200},
    }

    Variant = 'crossbow'
