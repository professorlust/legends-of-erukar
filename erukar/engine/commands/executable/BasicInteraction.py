from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class BasicInteraction(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'

    ActionPointCost = 1
    LimitToLocal = True

    def perform(self):
        '''
        interactionType | Behavior
        ===========================
        open             | on_open        
        close            | on_close
        '''
        interaction_method = 'on_' + self.args['interactionType']
        if not self.args['interaction_target']: return self.fail(BasicInteraction.NoTarget)
        if not hasattr(self.args['interaction_target'], interaction_method):
            raise Exception('Interaction Method {0} not defined for '.format(interaction_method, self.args['interaction_target']))
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail('Not enough action points!')

        result, was_success = getattr(self.args['interaction_target'], interaction_method)(self.args['player_lifeform'])
        self.append_result(self.player_info.uid, result)
        if was_success:
            self.args['player_lifeform'].consume_action_points(self.ActionPointCost)
            return self.succeed()
        return self.fail()
