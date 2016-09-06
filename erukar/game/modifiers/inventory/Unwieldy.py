from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Unwieldy(WeaponMod):
    Probability = 1
    Desirability = 0.5
    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Unwieldy " + weapon.name
