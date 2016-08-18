from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Grand(WeaponMod):
    Probability = 0.1
    Desirability = 16.0
    def apply_to(self, weapon):
        weapon.name = "Grand " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [min_dam*2, max_dam*2]       
