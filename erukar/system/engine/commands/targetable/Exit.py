from erukar.system.engine import Interaction
from ..TargetedCommand import TargetedCommand

class Exit(TargetedCommand):
    '''
    requires:
        target
    '''

    def perform(self):
        if self.invalid('target'): return self.fail('cannot exit without a target')
        
        if not isinstance(self.args['target'], Interaction):
            return self.fail('Target is not an interaction')

        if self.args['target'].ended:
            return self.fail('Target Interaction has already ended')

        self.args['target'].mark_for_exit(self.player_info)
        return self.succeed()
