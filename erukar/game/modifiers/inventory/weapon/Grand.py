from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Grand(WeaponMod):
    Probability = 0.5
    def apply_to(self, weapon):
        weapon.name = "Grand " + weapon.name
