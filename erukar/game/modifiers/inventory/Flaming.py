from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Flaming(WeaponMod):
    Probability = 1
    Desirability = 8.0
    Description = "The {EssentialPart} of the {BaseName} is wreathed in flames."

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name += " of the Flames"
        weapon.damages.append(Damage("Fire", [1,4], "", (np.random.uniform, (0,1))))
