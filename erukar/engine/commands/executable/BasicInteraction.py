from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class BasicInteraction(ActionCommand):
    ActionPointCost = 1

    def perform(self):
        '''
        interaction_type | Behavior
        ===========================
        open             | on_open        
        close            | on_close
        glance           | on_glance        
        '''
        interaction_method = 'on_' + self.args['interaction_type']
        if not hasattr(self.args['interaction_target'], interaction_method):
            raise Exception('Interaction Method {0} not defined'.format(interaction_method))
        if self.args['player_lifeform'].action_points < self.ActionPointCost:
            return self.fail('Not enough action points!')

        result, was_success = getattr(self.args['interaction_target'], interaction_method)(self.args['player_lifeform'])
        self.append_result(self.player_info.uuid, result)
        if was_success:
            self.args['player_lifeform'].action_points -= self.ActionPointCost
            return self.succeed()
        return self.fail()
