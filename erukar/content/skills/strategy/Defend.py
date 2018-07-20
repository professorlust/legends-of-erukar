from erukar.system.engine import SidebarAbility, Shield
import math


class Defend(SidebarAbility):
    Name = 'Defend'
    DefendSuccess = 'You ready your {}, providing {} additional deflection '\
        'and {} additional mitigation!'
    CurrentLevel = 'Allows a shield-bearer to brace against attacks, '\
        'providing a ({:0.0f}+{:0.0f}% per Action Point Consumed) bonus '\
        'to deflection and a ({:0.0f}+{:0.0f}% per Action Point Consumed) '\
        'bonus to mitigation. These values affect only the deflections '\
        'and mitigations provided by shields equipped. This command '\
        'consumes all remaining Action Points, including those '\
        'provided from a wait.'
    NextLevel = 'Deflection bonuses increase to ({:0.0f}+{:0.0f}% per '\
        'Action Point Consumed) and Mitigation bonuses increase to '\
        '({:0.0f}+{:0.0f}% per Action Point Consumed)'
    ActiveAbbreviation = 'DEF'

    def action_point_cost(self, cmd):
        player = cmd.args['player_lifeform']
        return player.action_points()

    def deflection_base(level):
        return 0.10 * (math.floor((level-1)/2)+1)

    def deflection_per_ap(level):
        return 0.20 + 0.05 * level

    def total_deflection(self, ap):
        return Defend.deflection_base(self.level)\
                + ap * Defend.deflection_per_ap(self.level)

    def mitigation_base(level):
        return 0.10 * (math.floor((level-1)/2)+1)

    def mitigation_per_ap(level):
        return 0.20 + 0.05 * level

    def total_mitigation(self, ap):
        return Defend.mitigation_base(self.level)\
                + ap * Defend.mitigation_per_ap(self.level)

    def current_level_description(self):
        dfl_base = Defend.deflection_base(self.level) * 100.0
        dfl_ap = Defend.deflection_per_ap(self.level) * 100.0
        mit_base = Defend.mitigation_base(self.level) * 100.0
        mit_ap = Defend.mitigation_per_ap(self.level) * 100.0
        return self.CurrentLevel.format(dfl_base, dfl_ap, mit_base, mit_ap)

    def next_level_description(self):
        dfl_base = Defend.deflection_base(self.level + 1) * 100.0
        dfl_ap = Defend.deflection_per_ap(self.level + 1) * 100.0
        mit_base = Defend.mitigation_base(self.level + 1) * 100.0
        mit_ap = Defend.mitigation_per_ap(self.level + 1) * 100.0
        return self.NextLevel.format(dfl_base, dfl_ap, mit_base, mit_ap)

    def can_activate(self):
        return True

    def perform(self, cmd):
        player = cmd.args['player_lifeform']
        if not self.can_activate():
            return cmd.fail('Cannot defend -- not activatable!')
        equipped_shields = list(self.shields(player))
        if len(equipped_shields) < 1:
            return cmd.fail('No Shields equipped!')
        shield = equipped_shields[0].alias()
        ap = player.action_points()
        player.consume_action_points(ap)
        dfl = self.total_deflection(ap) * 100.0
        mit = self.total_mitigation(ap) * 100.0
        cmd.append_result(player.uid, self.DefendSuccess.format(shield, dfl, mit))
        return cmd.succeed()

    def shields(self, player):
        for item in player.equipped_items():
            if isinstance(item, Shield):
                yield item
