from erukar.system.engine import Interaction, Item, Merchant
from ...TargetedCommand import TargetedCommand
from ...auto.Inventory import Inventory
import uuid

class Sell(TargetedCommand):
    '''
    requires:
        interaction
        target
    '''

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure: return failure

        if 'target' not in self.args or not isinstance(self.args['target'], Item):
            return self.fail('Target is invalid')

        item = self.args['target']
        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc

        if item not in player.inventory:
            return self.fail('Item does not belong to you!')

        self.get_quantity()
        actual_price = self.args['quantity'] * npc.template(Merchant).buying_price(item, player)

        return self.do_sell()\
            if npc.wealth >= actual_price\
            else self.fail('NPC cannot buy your {}'.format(item.alias()))

    def get_quantity(self):
        self.args['quantity'] = max(1, self.args.get('quantity', -1))
        self.args['quantity'] = min(getattr(self.args['target'], 'quantity', 1), self.args['quantity'])

    def do_sell(self):
        failure = self.do_split()
        if failure: return failure

        item = self.args['target']
        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc
        self.dirty(player)

        price = npc.template(Merchant).buy_from(player, item, self.args['quantity'])
        self.append_result(self.player_info.uid, 'You have sold your {} to {} for {} riphons.'.format(item.alias(), npc.alias(), price))
        
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            if not item or not hasattr(item, 'uuid'): continue
            if item.uuid == self.args['target'].uuid:
                return slot
        return ''

    def do_split(self):
        self.args['player_lifeform'].inventory.remove(self.args['target'])
        equipment_slot = self.get_equip_slot()
        if equipment_slot:
            setattr(self.args['player_lifeform'], equipment_slot, None)

        sold, remaining_stock = self.args['target'].split(self.args['target'], self.args['quantity'])
        self.args['interaction'].main_npc.inventory.append(sold)
        failure = sold.on_take(self.args['interaction'].main_npc)
        if remaining_stock:
            self.args['player_lifeform'].inventory.append(remaining_stock)
            remaining_stock.on_take(self.args['player_lifeform'])
        return failure

    def fix_ids_on_split(original, copied):
        original.uuid = copied.uuid
        copied.uuid = uuid.uuid4()
        original.id = copied.id
        del copied.id
