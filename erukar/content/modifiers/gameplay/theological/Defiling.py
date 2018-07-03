from erukar.system.engine import SpellInstance
from ...base.WeaponMod import WeaponMod
import erukar
import random


class Defiling(WeaponMod):
    Probability = 1
    PriceMod = 0.1

    PercentChance = 0.10
    DefilePower = -1.0
    DefileRadius = 4
    InventoryName = "Defiling"
    InventoryDescription = 'On successful hit, has a 10% chance to Desecrate the area around target'
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
        if random.random() >= Defiling.PercentChance:
            return
        chain = [erukar.content.CreateSanctityAura]
        kwargs = {
            'radius': Defiling.DefileRadius,
            'sanctity': Defiling.DefilePower
        }
        spell = SpellInstance(chain)
        instigator = cmd.args['player_lifeform']
        target = cmd.args['interaction_target']
        log = spell.execute(instigator, target, **kwargs)
        cmd.append_result(instigator.uid, ' '.join(log))
