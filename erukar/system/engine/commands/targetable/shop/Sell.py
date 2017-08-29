from erukar.system.engine import Interaction
from ..TargetedCommand import TargetedCommand

class Sell(TargetedCommand):
    '''
    requires:
        target
    '''

    def perform(self):
        self.append_result(self.player_info.uid, 'Selling!')
        return self.succeed()
