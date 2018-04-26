from .NpcTemplate import NpcTemplate
from erukar.system.engine import StackableItem

class Merchant(NpcTemplate):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = []

    def disposition(self, player):
        return 1.25

    def selling_price(self, item, seller):
        return int(item.price(self.world.location.economic_profile) * self.disposition(seller) * seller.haggling_sell_modifier())

    def buying_price(self, item, buyer):
        return int(item.price(self.world.location.economic_profile) * 1/self.disposition(buyer) * seller.haggling_buy_modifier())

    def buy_from(self, from_player, item, quantity):
        price = self.buying_price(item, from_player) * quantity
        from_player.wealth += price
        self.npc.wealth -= price
        return price

    def sell_to(self, to_player, item, quantity):
        price = self.selling_price(item, to_player) * quantity
        to_player.wealth -= price
        self.npc.wealth += price
        return price

    def interaction_text(self):
        return 'Trade with {}'.format(self.npc.alias())

    def get_state(self, for_player):
        return {
            'type': 'Shop',
            'title': '{}\'s Shop'.format(self.npc.alias()),
            'wealth': self.npc.wealth,
            'inventory': list(self.process_npc_inventory(for_player)),
            'player_inventory': list(self.process_player_inventory(for_player))
        }

    def process_player_inventory(self, player):
        mapped_items = set()
        for item in player.inventory:
            if item.__module__ in mapped_items or self.should_ignore_item(item): continue
            mapped_items.add(item.__module__)
            quantity = self.quantity(item, player.inventory)
            price = self.buying_price(item, player)
            yield self.format_item(item, player, quantity, price)

    def process_npc_inventory(self, for_player):
        mapped_items = set()
        for item in self.npc.inventory:
            if item.__module__ in mapped_items or self.should_ignore_item(item): continue
            mapped_items.add(item.__module__)
            quantity = self.quantity(item, self.npc.inventory)
            price = self.selling_price(item, for_player)
            yield self.format_item(item, for_player, quantity, price)

    def should_ignore_item(self, item):
        return len(self.desired_item_types) > 0 \
            and not any([isinstance(item, desired_type) for desired_type in self.desired_item_types])

    def format_item(self, item, for_player, quantity, price):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'quantifiable_alias': item.alias() if quantity <= 1 else '{} x{}'.format(item.alias(), quantity),
            'quantity': quantity,
            'price': price
        }
        if isinstance(item, StackableItem):
            object_output['quantifiable_alias'] = item.long_alias()
        return object_output

    def quantity(self, item, inventory):
        if isinstance(item, StackableItem):
            return item.quantity
        return len([x for x in inventory if x.__module__ == item.__module__])
