from erukar.system.engine import Item, Merchant
from ...TargetedCommand import TargetedCommand
from ...auto.Inventory import Inventory
import uuid

class Sell(TargetedCommand):
    Success = 'You have sold your {} to {} for {} riphons.'
    '''
    requires:
        interaction
        target
    '''

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure:
            return failure

        item = self.args.get('target')
        if not item or not isinstance(item, Item):
            return self.fail('Target is invalid')

        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc

        if item not in player.inventory:
            return self.fail('Item does not belong to you!')

        quantity = self.get_quantity(item)
        _price = npc.template(Merchant).buying_price(item, player)
        actual_price = quantity * _price

        if npc.wealth >= actual_price:
            return self.do_sell(quantity)
        return self.fail('NPC cannot buy your {}'.format(item.alias()))

    def get_quantity(self, item):
        quantity = max(1, self.args.get('quantity', -1))
        return min(getattr(item, 'quantity', 1), quantity)

    def do_sell(self, quantity):
        item = self.args['target']
        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc

        failure = self.do_split(player, npc, item, quantity)
        if failure:
            return failure
        self.dirty(player)

        price = npc.template(Merchant).buy_from(player, item, quantity)
        self.log(player, self.Success.format(item.alias(), npc.alias(), price))
        return self.succeed()

    def get_equip_slot(self):
        for slot in Inventory.InventorySlots:
            item = getattr(self.args['player_lifeform'], slot)
            if not item or not hasattr(item, 'uuid'):
                continue
            if item.uuid == self.args['target'].uuid:
                return slot
        return ''

    def do_split(self, player, npc, item, quantity):
        player.inventory.remove(item)
        sold, remaining_stock = item.split(item, quantity)
        npc.inventory.append(sold)
        failure = sold.on_take(self, npc)
        if remaining_stock:
            player.inventory.append(remaining_stock)
            remaining_stock.on_take(self)
            payload = Inventory.format_item(item, player)
            self.add_to_outbox(player, 'update item', payload)
        else:
            payload = {'uid', str(item.uuid)}
            self.add_to_outbox(player, 'remove item', payload)
        return failure

    def fix_ids_on_split(original, copied):
        original.uuid = copied.uuid
        copied.uuid = uuid.uuid4()
        original.id = copied.id
        del copied.id
