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
        if self.invalid('subject'): return self.fail(Drop.NoTarget)
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Drop.NotEnoughAP)
            
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)
        self.validate_target()
        return self.do_use()

    def validate_target(self):
        if self.invalid('target'):
            self.args['target'] = self.args['player_lifeform']

    def do_use(self):
        result = self.args['subject'].on_use(self.args['target'])
        if not result: return self.could_not_use()
        
        self.dirty(self.args['player_lifeform'])
        self.dirty(self.args['target'])
        self.append_result(self.player_info.uid, result)
        return self.succeed()

    def could_not_use(self):
        self.append_result(self.player_info.uid, 'Could not use {}'.format(self.args['subject'].alias()))
        return self.succeed()
