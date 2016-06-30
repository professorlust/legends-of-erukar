from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Broken(WeaponMod):
    Probability = 2
    def apply_to(self, weapon):
        weapon.name = "Broken " + weapon.name
        weapon.damage += "-2"
