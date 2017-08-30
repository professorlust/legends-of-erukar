from erukar.system.engine import Interaction, Npc
from ..TargetedCommand import TargetedCommand

class Start(TargetedCommand):
    '''
    requires:
        interaction_target
    '''

    def perform(self):
        if self.invalid('interaction_target'): return self.fail('No NPC was specified')

        if not isinstance(self.args['interaction_target'], Npc):
            return self.fail('Target is not an NPC')

        if not self.is_unique():
            return self.fail('Duplicate Interaction exists.')

        interaction = Interaction()
        interaction.main_npc = self.args['interaction_target']
        interaction.involved = [self.player_info]

        self.append_result(self.player_info.uid, 'Starting interaction with {}'.format(self.args['interaction_target']))
        return self.succeed_with_new_interaction(interaction)

    def is_unique(self):
        return not any(self.matches_interaction(interaction) for interaction in self.interactions)

    def matches_interaction(self, interaction):
        return interaction.main_npc is self.args['interaction_target'] and self.player_info in interaction.involved
