from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Rusty(WeaponMod):
    Probability = 5
    Desirability = 0.125

    DurabilityMultiplier = 0.667
    InventoryName = "Rusty"
    InventoryDescription = "Reduces maximum base damage by 2, reduces durability by 33%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.damages[0].damage[1] -= 2
        weapon.name = "Rusty " + weapon.name
