from erukar.system.engine import SpellInstance
from ...base.WeaponMod import WeaponMod
import erukar
import random


class Purifying(WeaponMod):
    Probability = 1
    PriceMod = 0.1

    PercentChance = 0.10
    PurifyPower = 1.0
    PurifyRadius = 4
    InventoryName = "Purifying"
    InventoryDescription = 'On successful hit, has a 10% chance to Hallow the area around target'
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
        if random.random() >= Purifying.PercentChance:
            return
        chain = [erukar.content.CreateSanctityAura]
        kwargs = {
            'radius': Purifying.PurifyRadius,
            'sanctity': Purifying.PurifyPower
        }
        spell = SpellInstance(chain)
        instigator = cmd.args['player_lifeform']
        target = cmd.args['interaction_target']
        log = spell.execute(instigator, target, **kwargs)
        cmd.append_result(instigator.uid, ' '.join(log))
