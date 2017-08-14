from erukar.system.engine import Interaction, Npc
from ..TargetedCommand import TargetedCommand

class Start(TargetedCommand):
    '''
    requires:
        target
    '''

    def perform(self):
        if self.invalid('target'): return self.fail('No NPC was specified')

        if not isinstance(self.args['target'], Npc):
            return self.fail('Target is not an NPC')

        interaction = Interaction()
        interaction.target = self.args['target']
        interaction.involved = [self.player_info]
        return self.succeed_with_new_interaction(interaction)
