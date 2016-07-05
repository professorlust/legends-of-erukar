from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Flaming(WeaponMod):
    Probability = 1
    def apply_to(self, weapon):
        weapon.name += " of the Flames"
