from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Fine(WeaponMod):
    Probability = 0.3
    Desirability = 4.0

    def apply_to(self, weapon):
        weapon.name = "Fine " + weapon.name
        min_dam, max_dam = weapon.damages[0].damage
        weapon.damages[0].damage = [min_dam+1, max_dam+1]       
