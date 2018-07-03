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

    def modify_post_inflict_damage(self, weapon, cmd):
        chain = [erukar.content.EnergyBurn]
        kwargs = {
            'percent': MageKiller.BurnPercent,
            'power': MageKiller.BurnPower
        }
        burn_spell = SpellInstance(chain)
        instigator = cmd.args['player_lifeform']
        target = cmd.args['interaction_target']
        log = burn_spell.execute(instigator, target, **kwargs)
        cmd.append_result(instigator.uid, ' '.join(log))
