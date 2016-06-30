from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Acid(WeaponMod):
    Probability = 1
    def apply_to(self, weapon):
        weapon.name = "Acid " + weapon.name
        weapon.damage += "+2"
