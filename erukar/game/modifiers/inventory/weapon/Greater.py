from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Greater(WeaponMod):
    Probability = 1
    def apply_to(self, weapon):
        weapon.name = "Greater " + weapon.name
