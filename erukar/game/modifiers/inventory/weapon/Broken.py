from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Broken(WeaponMod):
    Probability = 2
    def apply_to(self, weapon):
        weapon.name = "Broken " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [min_dam-1, max_dam-2]
