from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Rusty(WeaponMod):
    Probability = 5
    Desirability = 0.125
    Description = "The {EssentialPart} of this {BaseName} has corroded heavily and is covered in rust"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.damages[0].damage[1] -= 1
        weapon.name = "Rusty " + weapon.name
