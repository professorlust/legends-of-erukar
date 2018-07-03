from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Flaming(WeaponMod):
    Probability = 1
    PriceMod = 3.0

    InventoryName = "Flaming"
    InventoryDescription = "Adds 25 raw Fire damage to weapon which scales with Resolve"
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
        yield Damage('fire', [
            DamageScalar(
                Flaming.RawDamage,
                'resolve',
                scale_amount=Flaming.ScaleAmount,
                requirement=0)
        ])
