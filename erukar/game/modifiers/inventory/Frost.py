from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Frost(WeaponMod):
    Probability = 1
    Desirability = 8.0
    def apply_to(self, weapon):
        weapon.name = "Frosted " + weapon.name
        weapon.damages.append(Damage("Cold", [1,4], "", (np.random.uniform, (0,1))))
