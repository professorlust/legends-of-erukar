from erukar.system.engine import SearchScope
from ..ActionCommand import ActionCommand
from .Unequip import Unequip

class Drop(ActionCommand):
    NoTarget = 'subject not found'
    NotEnoughAP = 'Not enough AP to drop!'
    Successful = 'You dropped {}.'

    # Base. This is added to the Unequip cost if the item is equipped
    ActionPointCost = 1
    RebuildZonesOnSuccess = True

    '''
    Requires:
        subject
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        if self.invalid('subject'): return self.fail(Drop.NoTarget)
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Drop.NotEnoughAP)
            
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)
        self.args['player_lifeform'].inventory.remove(self.args['subject'])

        self.world.add_actor(self.args['subject'], self.args['player_lifeform'].coordinates)
        
        drop_result = self.args['subject'].on_drop(self.args['player_lifeform'], self.args['player_lifeform'])
        if drop_result: self.append_result(self.player_info.uid, drop_result)

        self.dirty(self.args['player_lifeform'])

        self.append_result(self.player_info.uid, Drop.Successful.format(self.args['subject'].describe()))
        return self.succeed()
