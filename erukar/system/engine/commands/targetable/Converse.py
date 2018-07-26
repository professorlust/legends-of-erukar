from ..TargetedCommand import TargetedCommand
import erukar


class Converse(TargetedCommand):
    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure:
            return failure

        interaction = self.args.get('interaction')
        conversation = Converse.get_conversation(interaction)
        player = self.args['player_lifeform']
        choice = self.args.get('choice_id', 'not-a-valid-choice')

        if not conversation.is_valid_choice(player, choice):
            return self.fail('Choice was note valid!')

        conversation.advance(player, choice)
        if not conversation.is_conversing(player):
            interaction.mark_for_exit(self.player_info)
        return self.succeed()

    def get_conversation(interaction):
        for template in interaction.main_npc.templates:
            if isinstance(template, erukar.Conversationalist):
                return template.conversation
        return None
