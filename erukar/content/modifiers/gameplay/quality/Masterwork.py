from ...base.WeaponMod import WeaponMod
import erukar


class Masterwork(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Masterwork"
    InventoryDescription = "+5 to Attack Rolls, 30% base damage increase"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Armor,
        erukar.system.Ammunition
    ]

    def on_calculate_attack_roll(self, result, target):
        return result + 5

    def modify_raw_base_damage(self, weapon, raw_damage):
        return raw_damage * 1.30
