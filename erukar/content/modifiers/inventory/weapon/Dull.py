from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Modifier
from erukar.ext.math import Modules
import numpy as np
import math

class Dull(WeaponMod):
    Probability = 2
    Desirability = 0.025
    PermissionType = Modifier.ALL_PERMITTED
    Description = "The {EssentialPart} of the {item_type} has been dulled from extensive, careless use."
    InventoryName = "Dulled"
    InventoryDescription = "Reduces slashing damage by 50% and converts 25% of initial to bludgeoning"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Dull " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [int(math.floor(min_dam/2)), int(math.floor(max_dam/2))]
        weapon.damages.append(dulled)
