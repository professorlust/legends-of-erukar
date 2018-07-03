from ...base.WeaponMod import WeaponMod
import erukar


class ElectricityResistance(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Electricity Resistance"
    InventoryDescription = "Adds 10% mitigation against Electricity"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
    ]

    def electricity_protection(self, item):
        return (0.10, 0)
