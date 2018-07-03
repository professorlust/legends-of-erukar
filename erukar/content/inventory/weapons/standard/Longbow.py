from erukar.system.engine.inventory import BowWeapon
import numpy as np

class Longbow(BowWeapon):
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

    BaseStatInfluences = {
        'dexterity':  {'requirement': 8, 'scaling_factor': 3, 'cutoff': 200},
    }
