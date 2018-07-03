from ...base.WeaponMod import WeaponMod
import erukar


class AcidResistance(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Acid Resistance"
    InventoryDescription = "Adds 10% mitigation against Aqueous Damage"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
    ]

    def aqueous_protection(self, item):
        return (0.10, 0)
