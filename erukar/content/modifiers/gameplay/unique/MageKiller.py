from erukar.system.engine import SpellInstance
from ...base.WeaponMod import WeaponMod
import erukar


class MageKiller(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    BurnPercent = 0.025
    BurnPower = 2.0
    InventoryName = "Magekiller"
    InventoryDescription = 'Burns 2.5% of enemy arcane energy on hit, dealing 2x that amount as arcane damage'
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def modify_post_inflict_damage(self, damage, cmd):
        chain = [
            erukar.content.PotionSource,
            erukar.content.EnergyBurn
        ]
        spell = SpellInstance(chain)
        spell.cmd_execute(cmd)
