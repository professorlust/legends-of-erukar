from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Swift(WeaponMod):
    Probability = 1
    def apply_to(self, weapon):
        weapon.name = "Swift " + weapon.name
