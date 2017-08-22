from erukar.system.engine import Interaction, Npc
from ..TargetedCommand import TargetedCommand

class Start(TargetedCommand):
    '''
    requires:
        target
    '''

    def perform(self):
        if self.invalid('interaction_target'): return self.fail('No NPC was specified')

        if not isinstance(self.args['interaction_target'], Npc):
            return self.fail('Target is not an NPC')

        interaction = Interaction()
        interaction.main_npc = self.args['interaction_target']
        interaction.involved = [self.player_info]

        self.append_result(self.player_info.uid, 'Starting interaction with {}'.format(self.args['interaction_target']))
        return self.succeed_with_new_interaction(interaction)
