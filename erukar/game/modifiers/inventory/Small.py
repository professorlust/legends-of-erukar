from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Small(WeaponMod):
    Probability = 1
    Desirability = 0.5
    Description = "The {EssentialPart} of the {BaseName} is inexcplicably small compared to the rest of the weapon."
    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Small " + weapon.name
