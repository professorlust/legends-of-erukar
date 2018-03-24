from erukar.system.engine import Interaction, Item, SearchScope
from ...TargetedCommand import TargetedCommand

class Purchase(TargetedCommand):
    '''
    requires:
        interaction
        target
        quantity (default 1)
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure: return failure

        if 'target' not in self.args or not isinstance(self.args['target'], Item):
            return self.fail('Target is invalid')
        
        if self.args['target'] not in self.args['interaction'].main_npc.inventory:
            return self.fail('Item does not belong to NPC!')

        self.get_quantity()
        actual_price = self.args['quantity'] * self.args['target'].price()
        if self.args['player_lifeform'].wealth >= actual_price:
            return self.do_purchase(actual_price)

        return self.fail('You do not have enough money to buy {}'.format(self.args['target'].alias()))

    def get_quantity(self):
        self.args['quantity'] = max(1, self.args.get('quantity', -1))
        self.args['quantity'] = min(getattr(self.args['target'], 'quantity', 1), self.args['quantity'])

    def do_purchase(self, price):
        failure = self.move_to_inventory()
        if failure: return failure

        self.args['interaction'].main_npc.wealth += price
        self.args['player_lifeform'].wealth -= price

        self.dirty(self.args['player_lifeform'])
        self.append_result(self.player_info.uid, 'You have bought {} from {} for {} riphons.'.format(self.args['target'].alias(), self.args['interaction'].main_npc.alias(), price))
        return self.succeed()

    def move_to_inventory(self):
        self.args['interaction'].main_npc.inventory.remove(self.args['target'])
        purchased, remaining_stock = self.args['target'].split(self.args['target'], self.args['quantity'])
        self.args['player_lifeform'].inventory.append(purchased)
        if remaining_stock:
            self.args['interaction'].main_npc.inventory.append(remaining_stock)
            remaining_stock.on_take(self.args['interaction'].main_npc)
        failure = purchased.on_take(self.args['player_lifeform'])
        return failure
