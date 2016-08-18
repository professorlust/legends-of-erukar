from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
import math

class Broken(WeaponMod):
    Probability = 2
    Desirability = 0.0625

    def apply_to(self, weapon):
        weapon.name = "Broken " + weapon.name
        max_dam = weapon.damages[0].damage[1]
        weapon.damages[0].damage = [0, int(math.floor(max_dam/2))]
