from ...base.WeaponMod import WeaponMod
import erukar


class Sharp(WeaponMod):
    Probability = 1
    PriceMod = 1.4

    InventoryName = "Sharp"
    InventoryDescription = 'Increases Slashing Damage percentage by 200% and increases base damage by 10%'
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.inventory.SwordWeapon,
        erukar.system.inventory.FinesseWeapon,
        erukar.system.inventory.AxeWeapon,
        erukar.system.inventory.PolearmWeapon,
        erukar.system.Ammunition
    ]

    def modify_slashing_percentage(self, weapon, result):
        return result * 2.00

    def modify_raw_base_damage(self, weapon, raw_damage):
        return raw_damage * 1.10
