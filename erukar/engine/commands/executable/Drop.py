from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.commands.executable.Unequip import Unequip

class Drop(ActionCommand):
    NoTarget = 'inventory_item not found'
    NotEnoughAP = 'Not enough AP to drop!'
    Successful = 'You dropped {}.'

    # Base. This is added to the Unequip cost if the item is equipped
    ActionPointCost = 1

    '''
    Requires:
        inventory_item
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        if 'inventory_item' not in self.args or not self.args['inventory_item']: return self.fail(Drop.NoTarget)
        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Drop.NotEnoughAP)
            
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)
        self.args['player_lifeform'].inventory.remove(self.args['inventory_item'])
        self.args['player_lifeform'].room.add(self.args['inventory_item'])
        
        drop_result = self.args['inventory_item'].on_drop(self.args['player_lifeform'].room, self.args['player_lifeform'])
        if drop_result: self.append_result(self.player_info.uuid, drop_result)

        self.append_result(self.player_info.uuid, Drop.Successful.format(self.args['inventory_item'].describe()))
        return self.succeed()
