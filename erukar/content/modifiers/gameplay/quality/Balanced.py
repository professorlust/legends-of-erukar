from ...base.WeaponMod import WeaponMod
import erukar


class Balanced(WeaponMod):
    Probability = 1
    PriceMod = 1.3

    InventoryName = "Balanced"
    InventoryDescription = "+5 to Attack Rolls"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.engine.inventory.MartialWeapon,
        erukar.system.engine.inventory.Ammunition
    ]

    def on_calculate_attack_roll(self, result, target):
        return result + 5
