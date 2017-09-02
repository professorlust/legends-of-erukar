from erukar.system.engine import Interaction, Item, SearchScope
from ...TargetedCommand import TargetedCommand

class Purchase(TargetedCommand):
    '''
    requires:
        interaction
        target
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        failure = self.check_for_failure_on_interaction()
        if failure: return failure

        if 'target' not in self.args or not isinstance(self.args['target'], Item):
            return self.fail('Target is invalid')

        if self.args['player_lifeform'].wealth > self.args['target'].price():
            return self.do_purchase()

        return self.fail('You do not have enough money to buy {}'.format(self.args['target'].alias()))

    def do_purchase(self):
        price = self.args['target'].price()
        self.args['interaction'].main_npc.wealth += price
        self.args['interaction'].main_npc.inventory.remove(self.args['target'])
        self.args['player_lifeform'].wealth -= price
        self.dirty(self.args['player_lifeform'])
        self.append_result(self.player_info.uid, 'You have bought {} from {} for {} riphons.'.format(self.args['target'].alias(), self.args['interaction'].main_npc.alias(), price))
        return self.move_to_inventory()

    def move_to_inventory(self):
        self.args['player_lifeform'].inventory.append(self.args['target'])
        result = self.args['target'].on_take(self.args['player_lifeform'])
        return result if result else self.succeed()
