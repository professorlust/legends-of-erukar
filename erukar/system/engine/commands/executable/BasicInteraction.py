from ..ActionCommand import ActionCommand


class BasicInteraction(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'

    ActionPointCost = 1
    LimitToLocal = True

    def perform(self):
        target = self.args['interaction_target']
        if not target:
            return self.fail(BasicInteraction.NoTarget)

        method = 'on_' + self.args['interactionType']
        if not hasattr(target, method):
            error_str = 'Interaction Method {} not defined for {}'
            raise Exception(error_str.format(method, target))

        player = self.args['player_lifeform']
        if player.action_points() < self.ActionPointCost:
            return self.fail('Not enough action points!')

        return getattr(target, method)(self)
