from erukar.system.engine import Weapon
import numpy as np

class LightCrossBow(Weapon):
    Probability = 1
    BaseName = "Light Crossbow"
    EssentialPart = "string"
    BaseWeight = 3
    AttackRange = 4
    RangePenalty = 2

    # Damage
    DamageRange = [1, 4]
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
        'dexterity':  {'requirement': 5, 'scaling_factor': 5, 'cutoff': 200},
    }

    Variant = 'crossbow'
