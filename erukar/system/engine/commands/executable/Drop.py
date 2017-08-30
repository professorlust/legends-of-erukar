from erukar.system.engine import SearchScope
from ..ActionCommand import ActionCommand
from ..auto.Inventory import Inventory

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
        del self.args['subject'].id

        equipment_slot = self.get_equip_slot()
        if equipment_slot:
            setattr(self.args['player_lifeform'], equipment_slot, None)

        self.world.add_actor(self.args['subject'], self.args['player_lifeform'].coordinates)
        
        drop_result = self.args['subject'].on_drop(self.args['player_lifeform'], self.args['player_lifeform'])
        if drop_result: self.append_result(self.player_info.uid, drop_result)

        self.dirty(self.args['player_lifeform'])

        self.append_result(self.player_info.uid, Drop.Successful.format(self.args['subject'].describe()))
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            
            if not item or not hasattr(item, 'uuid'): continue
            if item.uuid == self.args['subject'].uuid:
                return slot
        return ''
