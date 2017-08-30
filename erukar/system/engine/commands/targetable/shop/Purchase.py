from erukar.system.engine import Interaction
from ...TargetedCommand import TargetedCommand

class Purchase(TargetedCommand):
    '''
    requires:
        interaction
        target
    '''

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure: return failure

        self.append_result(self.player_info.uid, self.args['target'])

        self.append_result(self.player_info.uid, 'Buying!')
        return self.succeed()
