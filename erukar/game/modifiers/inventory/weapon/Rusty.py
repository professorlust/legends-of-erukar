from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Rusty(WeaponMod):
    Probability = 5
    def apply_to(self, weapon):
        weapon.name = "Rusty " + weapon.name
