from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Unwieldy(WeaponMod):
    Probability = 1
    Desirability = 0.5
    Description = "The {BaseName} looks to have been built awkwardly."
    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Unwieldy " + weapon.name
