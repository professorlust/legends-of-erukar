from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Bane(WeaponMod):
    Probability = 1
    Desirability = 8.0

    def apply_to(self, weapon):
        weapon.name = weapon.name + ", Bane of ___"
