from ...base.WeaponMod import WeaponMod
import erukar


class Dulled(WeaponMod):
    Probability = 1
    PriceMod = 0.65

    InventoryName = "Dulled"
    InventoryDescription = 'Reduces Piercing and Slashing damages by 50% and increases Bludgeoning damage by 200%; reduces base damage by 25%'
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.engine.inventory.FinesseWeapon,
        erukar.system.engine.inventory.Ammunition,
        erukar.system.engine.inventory.AxeWeapon,
        erukar.system.engine.inventory.PolearmWeapon,
        erukar.system.engine.inventory.SwordWeapon,
    ]

    def modify_piercing_percentage(self, weapon, result):
        return result * 0.5

    def modify_bludgeoning_percentage(self, weapon, result):
        return result * 0.5

    def modify_slashing_percentage(self, weapon, result):
        return result * 0.5

    def modify_raw_base_damage(self, weapon, raw_damage):
        return raw_damage * 0.75
