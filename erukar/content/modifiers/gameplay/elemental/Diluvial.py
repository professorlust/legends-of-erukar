from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Damage, DamageScalar
import erukar


class Diluvial(WeaponMod):
    Probability = 1
    PriceMod = 3.0

    InventoryName = "Diluvial"
    InventoryDescription = "Adds 25 raw Aqueous damage to weapon which scales with Resolve"
    InventoryFlavorText = ''

    RawDamage = 25
    ScaleAmount = 1.75

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
        yield Damage('aqueous', [
            DamageScalar(
                Diluvial.RawDamage,
                'resolve',
                scale_amount=Diluvial.ScaleAmount,
                requirement=0)
        ])
