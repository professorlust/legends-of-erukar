from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model import Damage, Modifier
from erukar.game.inventory.weapons import *
import numpy as np
import math

class Dull(WeaponMod):
    Probability = 2
    Desirability = 0.025
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Axe, Halberd, Rapier, Spear, Sword]
    Description = "The {EssentialPart} of the {item_type} has been dulled from extensive, careless use."

    def apply_to(self, weapon):
        weapon.name = "Dull " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [int(math.floor(min_dam/2)), int(math.floor(max_dam/2))]
        weapon.damages.append(Damage("Bludgeoning", \
                                     [int(math.floor(min_dam/4)), \
                                     int(math.floor(max_dam/4))], \
                                     "", (np.random.uniform, (0,1))))

