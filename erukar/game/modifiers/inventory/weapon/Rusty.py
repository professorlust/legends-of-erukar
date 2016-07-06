from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Rusty(WeaponMod):
    Probability = 5
    def apply_to(self, weapon):
        weapon.damages[0].damage[1] -= 1
        weapon.name = "Rusty " + weapon.name
