from erukar.system.engine import Lifeform, SearchScope
from ..ActionCommand import ActionCommand
from ..auto.Inventory import Inventory

class Unequip(ActionCommand):
    NotFound = "No equipped item was found"
    RebuildZonesOnSuccess = True

    '''
    Requires:
        inventory_item
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        if 'inventory_item' not in self.args or not self.args['inventory_item']:
            return self.fail(Unequip.NotFound)
        equipment_slot = self.get_equip_slot()
        if not equipment_slot: return self.fail(Unequip.NotFound)

        if self.args['player_lifeform'].action_points() < self.args['inventory_item'].ActionPointCostToUnequip:
            return self.fail('Not enough action points to unequip {} from {}'.format(self.args['inventory_item'].alias(), equipment_slot))
            
        self.args['player_lifeform'].consume_action_points(self.args['inventory_item'].ActionPointCostToUnequip)
        setattr(self.args['player_lifeform'], equipment_slot, None)
        result = self.args['inventory_item'].on_unequip(self.args['player_lifeform'])
        if result: self.append_result(self.player_info.uuid, result)

        self.dirty(self.args['player_lifeform'])
        result = '{} unequipped from {} successfully.'.format(self.args['inventory_item'].describe(), equipment_slot)
        self.append_result(self.player_info.uid, result)
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            
            if not item or not hasattr(item, 'uuid'): continue
            if item.uuid == self.args['inventory_item'].uuid:
                return slot
        return ''
