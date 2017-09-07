from ..ActionCommand import ActionCommand
from erukar.system.engine import TransitionPiece

class Transition(ActionCommand):
    ActionPointCost = 1

    '''
    requires:
        target
    '''
    def perform(self):
        if self.invalid('target'): return self.fail('Target is invalid')

        if not isinstance(self.args['target'], TransitionPiece):
            return self.fail('Transition target is not a TransitionPiece')

        self.args['player_info'].mark_for_transition(self.args['target'].destination)
        return self.succeed()
