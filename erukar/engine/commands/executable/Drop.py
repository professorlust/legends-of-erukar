from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.commands.executable.Unequip import Unequip

class Drop(ActionCommand):
    NoTarget = 'interaction_target not found'
    NotEnoughAP = 'Not enough AP to drop!'
    Successful = 'You dropped {}.'

    # Base. This is added to the Unequip cost if the item is equipped
    ActionPointCost = 1

    '''
    Requires:
        interaction_target
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        if 'interaction_target' not in self.args or not self.args['interaction_target']: return self.fail(Drop.NoTarget)
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Drop.NotEnoughAP)
            
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)
        self.args['player_lifeform'].inventory.remove(self.args['interaction_target'])
        room = self.world.get_room_at(self.args['player_lifeform'].coordinates)
        room.add(self.args['interaction_target'])
        
        drop_result = self.args['interaction_target'].on_drop(self.args['player_lifeform'].room, self.args['player_lifeform'])
        if drop_result: self.append_result(self.player_info.uid, drop_result)

        self.append_result(self.player_info.uid, Drop.Successful.format(self.args['interaction_target'].describe()))
        return self.succeed()
