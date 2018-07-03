from ...base.WeaponMod import WeaponMod
import erukar


class Unmaintained(WeaponMod):
    Probability = 1
    PriceMod = 0.4

    InventoryName = "Unmaintained"
    InventoryDescription = "33% reduction in base damage"
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
        return raw_damage * 0.667
