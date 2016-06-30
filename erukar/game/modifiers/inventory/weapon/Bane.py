from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Bane(WeaponMod):
    Probability = 1
    def apply_to(self, weapon):
        weapon.name = weapon.name + ", Bane of ___"
        weapon.damage += "+3"
