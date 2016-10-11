from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Greater(WeaponMod):
    Probability = 0.25
    Desirability = 8.0
    Description = "The {BaseName} is wonderfully crafted by a master weaponmaker."

    InventoryName = "Great"
    InventoryDescription = "Increases maximum scaling by 130%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Greater " + weapon.name
        for si in weapon.stat_influences:
            weapon.stat_influences[si]['max_scale'] *= 1.3
