from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Burning(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Burning"
    InventoryDescription = "Adds 15 raw Fire damage to weapon which scales with Resolve"
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
        yield Damage('fire', [
            DamageScalar(
                Burning.RawDamage,
                'resolve',
                scale_amount=Burning.ScaleAmount,
                requirement=0)
        ])
