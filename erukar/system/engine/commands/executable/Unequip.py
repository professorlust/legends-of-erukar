from erukar.system.engine import SearchScope
from ..ActionCommand import ActionCommand
from ..auto.Inventory import Inventory


class Unequip(ActionCommand):
    NotFound = "No equipped item was found"
    RebuildZonesOnSuccess = True
    NotEnoughAP = 'Not enough action points to unequip {} from {}'
    Success = '{} unequipped from {} successfully.'

    '''
    Requires:
        inventory_item
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        target = self.args.get('inventory_item', None)
        if not target:
            return self.fail(Unequip.NotFound)

        slot = self.get_equip_slot()
        if not slot:
            return self.fail(Unequip.NotFound)

        player = self.args.get('player_lifeform')
        if player.action_points() < target.ActionPointCostToUnequip:
            return self.fail(self.NotEnoughAP.format(target.alias(), slot))

        player.consume_action_points(target.ActionPointCostToUnequip)
        setattr(player, slot, None)
        target.on_unequip(self)
        payload = Inventory.format_equipment(player, slot)
        self.add_to_outbox(player, 'equip', payload)

        self.dirty(player)
        self.log(player, self.Success.format(target.describe(), slot))
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            if not item or not hasattr(item, 'uuid'):
                continue
            if item.uuid == self.args['inventory_item'].uuid:
                return slot
        return ''
