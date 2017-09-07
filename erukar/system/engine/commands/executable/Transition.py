from ..ActionCommand import ActionCommand
from erukar.system.engine import TransitionPiece

class Transition(ActionCommand):
    ActionPointCost = 1

    '''
    requires:
        target
    '''
    def perform(self):
        if self.invalid('interaction_target'): return self.fail('Target is invalid')

        if not isinstance(self.args['interaction_target'], TransitionPiece):
            return self.fail('Transition target is not a TransitionPiece')

        self.player_info.mark_for_transition(self.args['interaction_target'].destination)
        return self.succeed()
