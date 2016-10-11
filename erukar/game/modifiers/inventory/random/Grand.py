from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Grand(WeaponMod):
    Probability = 0.1
    Desirability = 16.0
    Description = "The craftsmanship of the {BaseName} is staggering, as if it were created by the Gods themselves."

    InventoryName = "Grand"
    InventoryDescription = "Increases maximum scaling by 150%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Grand " + weapon.name
        for si in weapon.stat_influences:
            weapon.stat_influences[si]['max_scale'] *= 1.5
