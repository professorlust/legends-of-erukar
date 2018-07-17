from erukar.system.engine import SearchScope
from ..ActionCommand import ActionCommand


class Use(ActionCommand):
    ActionPointCost = 1
    RebuildZonesOnSuccess = True

    '''
    Requires:
        subject

    Optional:
        target
    '''

    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        if self.invalid('subject'):
            return self.fail('No target!')
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail('You do not have enough AP!')

        self.args['player_lifeform'].consume_action_points(1)
        self.validate_target()
        return self.do_use()

    def validate_target(self):
        if self.invalid('target'):
            self.args['target'] = self.args['player_lifeform']

    def do_use(self):
        self.dirty(self.args['player_lifeform'])
        self.dirty(self.args['target'])
        return self.args['subject'].on_use(self)
