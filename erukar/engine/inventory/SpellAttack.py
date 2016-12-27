from .Weapon import Weapon
import numpy as np

class SpellAttack(Weapon):
    Persistent = False
    Probability = 0
    BaseName = "Spell Attack"
    AttackRange = 0
    EquipmentLocations = ['left', 'right']

    DamageRange = [1,4]
    DamageModifier = "acuity"

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    BaseStateInfluences = {
    }
