from erukar.system.engine import HealingTool


class Salve(HealingTool):
    BaseName = "Salve"

    def heal_amount(level):
        return 10 * level

    def on_heal(self, cmd, skill):
        player = cmd.args['interaction_target']
        self.consume()
        gained = self.heal_amount(skill.level)
        pre_health = player.health
        player.health = max(player.max_health, player.health + gained)
        d_health = player.health - pre_health
        cmd.log(player, self.HealSuccess.format(d_health))
        return cmd.succeed()
