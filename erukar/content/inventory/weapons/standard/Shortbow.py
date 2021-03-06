from erukar.system.engine.inventory import BowWeapon
import numpy as np

class Shortbow(BowWeapon):
    Probability = 1
    BaseName = "Shortbow"
    EssentialPart = "bowstrings"
    BaseWeight = 2.0
    AttackRange = 3
    RangePenalty = 2

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
