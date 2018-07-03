from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Demonic(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Demonic"
    InventoryDescription = "Adds 15 raw Demonic damage to weapon which scales with Sense"
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
        yield Damage('demonic', [DamageScalar(
                Demonic.RawDamage,
                'sense',
                scale_amount=Demonic.ScaleAmount,
                requirement=0)])
