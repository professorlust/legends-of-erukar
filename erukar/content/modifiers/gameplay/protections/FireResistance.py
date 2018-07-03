from ...base.WeaponMod import WeaponMod
import erukar


class FireResistance(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Fire Resistance"
    InventoryDescription = "Adds 10% mitigation against Fire"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
    ]

    def fire_protection(self, item):
        return (0.10, 0)
