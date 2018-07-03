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

    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        lifeform = self.args['player_lifeform']
        if self.invalid('subject'):
            return self.fail(Drop.NoTarget)
        if lifeform.action_points() < self.ActionPointCost:
            return self.fail(Drop.NotEnoughAP)
        lifeform.consume_action_points(self.ActionPointCost)
        lifeform.inventory.remove(self.args['subject'])
        del self.args['subject'].id

        equipment_slot = self.get_equip_slot()
        if equipment_slot:
            setattr(lifeform, equipment_slot, None)

        self.world.add_actor(self.args['subject'], lifeform.coordinates)
        self.world.refresh_tiles()
        drop_result = self.args['subject'].on_drop(lifeform, lifeform)
        if drop_result:
            self.append_result(self.player_info.uid, drop_result)
        self.dirty(lifeform)

        result_text = Drop.Successful.format(self.args['subject'].describe())
        self.append_result(self.player_info.uid, result_text)
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            if not item or not hasattr(item, 'uuid'):
                continue
            if item.uuid == self.args['subject'].uuid:
                return slot
        return ''
