from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Bane(WeaponMod):
    Probability = 1
    Desirability = 8.0
    Description = 'Carved into the {DecorationLocation} of the {item_type} are small glowing runes which spell out "bane" in an ancient language.'

    InventoryDescription = "Deals 1.25x damage against ____ creatures"
    InventoryName = "____ Bane"

    def apply_to(self, weapon):
        weapon.name = weapon.name + ", Bane of ___"
        super().apply_to(weapon)
