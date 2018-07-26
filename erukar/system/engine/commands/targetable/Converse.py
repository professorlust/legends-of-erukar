from ..TargetedCommand import TargetedCommand


class Converse(TargetedCommand):
    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure:
            return failure

        interaction = self.args.get('interaction')
        conversation = interaction.main_npc.conversation
        player = self.args['player_lifeform']
        choice = self.args.get('choice_id', 'not-a-valid-choice')

        if not conversation.is_valid_choice(player, choice):
            return self.fail('Choice was note valid!')

        conversation.advance(player, choice)
        if not conversation.is_conversing(player):
            interaction.mark_for_exit(self.player_info)
        return self.succeed()
