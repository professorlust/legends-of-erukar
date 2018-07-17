from erukar.system.engine import Item, SearchScope, Merchant
from ...TargetedCommand import TargetedCommand
from ...auto.Inventory import Inventory


class Purchase(TargetedCommand):
    TooPoor = 'You do not have enough money to buy {}'
    Success = 'You have bought {} from {} for {} riphons.'

    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure:
            return failure

        item = self.args.get('target', None)
        if not item or not isinstance(item, Item):
            return self.fail('Target is invalid')

        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc

        if item not in npc.inventory:
            return self.fail('Item does not belong to NPC!')

        quantity = self.get_quantity(item)
        individual_price = npc.template(Merchant).selling_price(item, player)
        actual_price = quantity * individual_price
        if player.wealth >= actual_price:
            return self.do_purchase(actual_price, quantity)

        return self.fail(self.TooPoor.format(item.alias()))

    def get_quantity(self, item):
        quantity = max(1, self.args.get('quantity', -1))
        return min(getattr(item, 'quantity', 1), quantity)

    def do_purchase(self, price, quantity):
        item = self.args['target']
        player = self.args['player_lifeform']
        npc = self.args['interaction'].main_npc

        failure = self.move_to_inventory(player, npc, item, quantity)
        if failure:
            return failure

        self.dirty(player)
        price = npc.template(Merchant).sell_to(player, item, quantity)

        self.log(player, self.Success.format(item.alias(), npc.alias(), price))
        return self.succeed()

    def move_to_inventory(self, player, npc, item, quantity):
        npc.inventory.remove(item)
        purchased, remaining_stock = item.split(item, quantity)
        player.inventory.append(purchased)
        payload = Inventory.format_item(item, player)
        self.add_to_outbox(player, 'add item', payload)
        if remaining_stock:
            npc.inventory.append(remaining_stock)
            remaining_stock.on_take(self, npc)
        return purchased.on_take(self)
