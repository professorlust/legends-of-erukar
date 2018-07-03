from erukar.system.engine.inventory import CrossbowWeapon
import numpy as np

class HeavyCrossbow(CrossbowWeapon):
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
