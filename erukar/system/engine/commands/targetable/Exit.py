from erukar.system.engine import Interaction
from ..TargetedCommand import TargetedCommand

class Exit(TargetedCommand):
    '''
    requires:
        interaction
    '''

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure: return failure

        self.args['interaction'].mark_for_exit(self.player_info)
        return self.succeed()
