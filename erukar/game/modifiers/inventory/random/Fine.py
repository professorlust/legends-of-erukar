from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Fine(WeaponMod):
    Probability = 0.3
    Desirability = 4.0
    Description = "The craftsmanship of the {BaseName} truly stands out."

    InventoryName = "Refined"
    InventoryDescription = "Increases scaling factor by 150%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Fine " + weapon.name
        for si in weapon.stat_influences:
            weapon.stat_influences[si]['scaling_factor'] *= 1.5
