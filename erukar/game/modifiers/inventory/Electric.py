from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Electric(WeaponMod):
    Probability = 1
    Desirability = 8.0
    Description = "Sparks and electrical arcs regularly dance off of the {EssentialPart} of the {item_type}"

    def apply_to(self, weapon):
        weapon.name += " of Lightning"
        weapon.damages.append(Damage("Electric", [1,4], "", (np.random.uniform, (0,1))))
