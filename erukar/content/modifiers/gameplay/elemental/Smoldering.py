from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Smoldering(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Smoldering"
    InventoryDescription = "Adds 10 raw Fire damage to weapon which scales with Resolve"
    InventoryFlavorText = ''

    RawDamage = 10
    ScaleAmount = 1.25

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
                Smoldering.RawDamage,
                'resolve',
                requirement=0,
                scale_amount=Smoldering.ScaleAmount)
        ])
