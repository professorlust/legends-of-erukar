from erukar.system.engine import Interaction, Npc
from ..TargetedCommand import TargetedCommand


class Start(TargetedCommand):
    '''
    requires:
        interaction_target
    '''

    def perform(self):
        if self.invalid('interaction_target'):
            return self.fail('No NPC was specified')

        if not isinstance(self.args['interaction_target'], Npc):
            return self.fail('Target is not an NPC')

        if not self.is_unique():
            return self.fail('Duplicate Interaction exists.')

        interaction = Interaction()
        interaction.main_npc = self.args['interaction_target']
        interaction.involved = [self.player_info]
        return self.succeed_with_new_interaction(interaction)

    def is_unique(self):
        for interaction in self.interactions:
            if self.matches_interaction(interaction):
                return False
        return True

    def matches_interaction(self, interaction):
        return interaction.main_npc is self.args['interaction_target']\
                and self.player_info in interaction.involved
