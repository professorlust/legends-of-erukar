from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Acid(WeaponMod):
    Probability = 1
    Desirability = 8.0
    Description = "Acid drips from the {BaseName}'s {EssentialPart}."

    def apply_to(self, weapon):
        weapon.name = "Acid " + weapon.name
        weapon.damages.append(Damage("Acid", [1,4], "", (np.random.uniform, (0,1))))
