from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Malevolent(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Malevolent"
    InventoryDescription = "Adds 15 raw Demonic damage to weapon which scales highly in desecrated areas and minimally in hallowed areas"
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
        true_scale = Malevolent.ScaleAmount * 2 * max(-1, min(1, (sanctity/-1)))

        yield Damage('demonic', [DamageScalar(
                Malevolent.RawDamage,
                'sense',
                scale_amount=true_scale,
                requirement=0)])
