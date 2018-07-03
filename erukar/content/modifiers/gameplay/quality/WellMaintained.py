from ...base.WeaponMod import WeaponMod
import erukar


class WellMaintained(WeaponMod):
    Probability = 1
    PriceMod = 1.1

    InventoryName = "Well Maintained"
    InventoryDescription = "25% increase in base damage"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def modify_raw_base_damage(self, weapon, raw_damage):
        return raw_damage * 1.25
