from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Charged(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Charged"
    InventoryDescription = "Adds 15 raw Electric damage to weapon which scales with Resolve"
    InventoryFlavorText = ''

    RawDamage = 15
    ScaleAmount = 1.5

    PersistentAttributes = ['raw_damage', 'scale_percentage']

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def get_additional_damages(self, weapon, is_attack=False):
        yield Damage('electric', [
            DamageScalar(
                Charged.RawDamage,
                'resolve',
                scale_amount=Charged.ScaleAmount, requirement=0)
        ])
