from erukar.system.engine import SidebarAbility, HealingTool


class Heal(SidebarAbility):
    Name = 'Heal'
    HealSuccess = 'You heal yourself for {} health!'
    ActiveAbbreviation = 'HEAL'

    def action_point_cost(self, cmd):
        return 1

    def current_level_description(self):
        health = Heal.heal_amount(self.level)
        cost = 1
        s = 'Consumes healing tools to regain {} health. Costs {} AP'
        return s.format(health, cost)

    def next_level_description(self):
        health = Heal.heal_amount(self.level+1)
        heal_str = 'Increases heal amount by {}'
        d_health = health - Heal.heal_amount(self.level)
        return heal_str.format(d_health)

    def heal_amount(level):
        return 10 * level

    def can_activate(self):
        return True

    def perform(self, cmd):
        player = cmd.args['player_lifeform']
        if not self.can_activate():
            return cmd.fail('Cannot heal!')
        item = player.find_in_inventory(HealingTool)
        if not item:
            return cmd.fail('No Healing Tools found!')
        cmd.args['interaction_target'] = cmd.get('interaction_target', player)
        player.consume_action_points(1)
        return item.on_heal(cmd)
