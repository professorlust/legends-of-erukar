from erukar.system.engine import SidebarAbility
from erukar.content.conditions import Enraged


class Rage(SidebarAbility):
    Name = 'Rage'
    RageSuccess = 'You become enraged, losing control of yourself! '\
        'Your Strength score is increaesd to {} and your Vitality '\
        'is increased to {}. Your Acuity and Sense scores are both '\
        'reduced by {}.'
    CurrentLevel = 'Allows this character to enter an enraged state, '\
        'providing a bonus to Strength and Vitality equal to the ' \
        'character\'s Resolve score (to a maximum of +{}. The character '\
        'also suffers that same value as penalty to Acuity and Sense '\
        'for the same duration. Effect lasts for 10 ticks.'
    NextLevel = 'Improves maximum Resolve bonus to {} from {}.'
    ActiveAbbreviation = 'RAGE'

    def action_point_cost(self, cmd):
        return 1

    def max_resolve_bonus(level):
        return 5 * level

    def total_resolve(self, player):
        return min(player.resolve, Rage.max_resolve_bonus(self.level))

    def current_level_description(self):
        bonus = Rage.max_resolve_bonus(self.level)
        return self.CurrentLevel.format(bonus)

    def next_level_description(self):
        now = Rage.max_resolve_bonus(self.level)
        future = Rage.max_resolve_bonus(self.level + 1)
        return self.NextLevel.format(future, now)

    def can_activate(self):
        return True

    def perform(self, cmd):
        player = cmd.args['player_lifeform']
        if not self.can_activate():
            return cmd.fail('Cannot rage -- not activatable!')
        if self.is_raging(player):
            return cmd.fail('Cannot Enrage -- Already Raging!')
        player.consume_action_points(1)
        bonus = self.total_resolve(player)
        rage = Enraged(player, player)
        rage.resolve_amount = bonus
        msg = self.RageSuccess.format(
            player.get('strength'),
            player.get('vitality'),
            bonus)
        cmd.append_result(player.uid, msg)
        return cmd.succeed()

    def is_raging(self, player):
        return any(isinstance(x, Enraged) for x in player.conditions)
