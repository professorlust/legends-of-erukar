from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Large(WeaponMod):
    Probability = 1
    Desirability = 2.0
    Description = "The {EssentialPart} is much larger than the rest of the {BaseName}."
    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Large " + weapon.name
