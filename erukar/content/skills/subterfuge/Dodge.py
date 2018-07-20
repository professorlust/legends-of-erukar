from erukar.system.engine import SidebarAbility
from erukar.content.conditions import Dodging
import math


class Dodge(SidebarAbility):
    Name = 'Dodge'
    DodgeSuccess = 'You prepare to dodge an enemy attack, granting '\
        '{:.0f}% extra evasion (now at {})'
    CurrentLevel = 'Consumes all available Action Points to provide '\
        'bonuses to evasion. The total bonus provided by activating '\
        'this ability is +{:.0f}+{:.0f}% per AP Consumed.'
    NextLevel = 'Further increases the bonuses provided to +{:.0f}+{:.0f}% '\
        'per AP consumed'
    ActiveAbbreviation = 'DDG'

    def action_point_cost(self, cmd):
        player = cmd.args['player_lifeform']
        return player.action_points()

    def evasion_base(level):
        return 0.10 * (math.floor((level-1)/2)+1)

    def evasion_per_ap(level):
        return 0.20 + 0.05 * level

    def total_evasion(self, ap):
        return Dodge.evasion_base(self.level)\
                + ap * Dodge.evasion_per_ap(self.level)

    def current_level_description(self):
        evd_base = Dodge.evasion_base(self.level) * 100.0
        evd_ap = Dodge.evasion_per_ap(self.level) * 100.0
        return self.CurrentLevel.format(evd_base, evd_ap)

    def next_level_description(self):
        evd_base = Dodge.evasion_base(self.level + 1) * 100.0
        evd_ap = Dodge.evasion_per_ap(self.level + 1) * 100.0
        return self.CurrentLevel.format(evd_base, evd_ap)

    def can_activate(self):
        return True

    def perform(self, cmd):
        player = cmd.args['player_lifeform']
        if not self.can_activate():
            return cmd.fail('Cannot dodge -- not activatable!')
        ap = player.action_points()
        player.consume_action_points(ap)
        bonus = self.total_evasion(ap)
        dodge = Dodging(player, player)
        dodge.EvasionBonus = bonus
        msg = self.DodgeSuccess.format(bonus * 100.0, player.evasion())
        cmd.append_result(player.uid, msg)
        return cmd.succeed()
