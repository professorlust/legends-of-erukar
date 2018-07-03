from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation
import erukar


class Unbalanced(WeaponMod):
    Probability = 1
    PriceMod = 0.7

    InventoryName = "Unbalanced"
    InventoryDescription = "-5 to Attack Rolls"
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
        return result - 5
