from ...base.WeaponMod import WeaponMod
import erukar
import random


class Serrated(WeaponMod):
    Probability = 1
    PriceMod = 1.2
    BleedingPercentage = 0.2
    InstigatorBleedingDescription = 'Your {} cuts a gash into {}, causing Bleeding!'
    TargetBleedingDescription = "{}'s {} slices open your flesh, causing Bleeding!"

    InventoryName = "Serrated"
    InventoryDescription = 'Increases Piercing Damage percentage by 25% and adds chance to inflict Bleeding'
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.inventory.SwordWeapon,
        erukar.system.inventory.FinesseWeapon,
        erukar.system.inventory.AxeWeapon,
        erukar.system.inventory.PolearmWeapon,
        erukar.system.Ammunition
    ]

    def modify_piercing_percentage(self, weapon, result):
        return result * 1.25

    def modify_post_inflict_damage(self, weapon, cmd):
        if random.random() < self.BleedingPercentage:
            self.inflict_bleeding(cmd)
            self.inform_instigator(weapon, cmd)
            self.inform_target(weapon, cmd)

    def inflict_bleeding(self, cmd):
        target = cmd.args['interaction_target']
        instigator = cmd.args['player_lifeform']
        erukar.content.conditions.Bleeding(target, instigator)

    def inform_instigator(self, weapon, cmd):
        target = cmd.args['interaction_target']
        description = self.InstigatorBleedingDescription.format(
            weapon.alias(),
            target.alias())
        cmd.append_result(cmd.player_info.uid, description)

    def inform_target(self, weapon, cmd):
        target = cmd.args['interaction_target']
        instigator = cmd.args['player_lifeform']
        target_uid = getattr(target, 'uid', None)
        description = self.TargetBleedingDescription.format(
            instigator.alias(),
            weapon.alias())
        cmd.append_result(target_uid, description)
