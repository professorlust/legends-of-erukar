from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Grand(WeaponMod):
    Probability = 0.1
    Desirability = 16.0
    Description = "The craftsmanship of the {BaseName} is staggering, as if it were created by the Gods themselves."

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Grand " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [min_dam*2, max_dam*2]       
