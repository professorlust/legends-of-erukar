from .Weapon import Weapon
import numpy as np

class UnarmedStrike(Weapon):
    Persistent = False
    Probability = 0
    BaseName = "Unarmed Strike"
    AttackRange = 0
    EquipmentLocations = ['left', 'right']

    DamageRange = [1,4]
    DamageType = "bludgeoning"
    DamageModifier = "strength"

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    BaseStateInfluences = {
        'strength': {'requirement':0, 'scaling_factor':1, 'max_scale':1}
    }
