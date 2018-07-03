from ...base.WeaponMod import WeaponMod
import erukar


class ColdResistance(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Cold Resistance"
    InventoryDescription = "Adds 10% mitigation against Ice"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
    ]

    def ice_protection(self, item):
        return (0.10, 0)
