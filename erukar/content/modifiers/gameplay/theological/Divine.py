from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Divine(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Divine"
    InventoryDescription = "Adds 15 raw Divine damage to weapon which scales highly in hallowed areas and minimally in desecrated areas"
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
        loc = weapon.owner.coordinates
        world = weapon.owner.world
        sanctity = world.sanctity_at(loc)
        true_scale = Divine.ScaleAmount * 2 * max(-1, min(1, sanctity))

        yield Damage('divine', [DamageScalar(
                Divine.RawDamage,
                'sense',
                scale_amount=true_scale,
                requirement=0)])
