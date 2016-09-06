from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Swift(WeaponMod):
    Probability = 1
    Desirability = 2.0
    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Swift " + weapon.name
