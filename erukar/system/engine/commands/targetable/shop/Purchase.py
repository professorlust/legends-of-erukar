from erukar.system.engine import Interaction
from ...TargetedCommand import TargetedCommand

class Purchase(TargetedCommand):
    '''
    requires:
        target
    '''

    def perform(self):
        self.append_result(self.player_info.uid, 'Buying!')
        return self.succeed()
