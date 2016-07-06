from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Grand(WeaponMod):
    Probability = 0.5
    def apply_to(self, weapon):
        weapon.name = "Grand " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [min_dam+4, max_dam+4]       
