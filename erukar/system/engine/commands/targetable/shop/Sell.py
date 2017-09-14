from erukar.system.engine import Interaction, Item
from ...TargetedCommand import TargetedCommand
from ...auto.Inventory import Inventory

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

        if self.args['target'] not in self.args['player_lifeform'].inventory:
            return self.fail('Item does not belong to you!')

        self.get_quantity()
        actual_price = self.args['quantity'] * self.args['target'].price()
        if self.args['interaction'].main_npc.wealth >= actual_price:
            return self.do_sell(actual_price)

        return self.fail('NPC cannot buy your {}'.format(self.args['target'].alias()))

    def get_quantity(self):
        self.args['quantity'] = max(1, self.args.get('quantity', -1))
        self.args['quantity'] = min(getattr(self.args['target'], 'quantity', 1), self.args['quantity'])

    def do_sell(self, price):
        failure = self.do_split()
        if failure: return failure

        self.args['player_lifeform'].wealth += price
        self.args['interaction'].main_npc.wealth -= price

        self.dirty(self.args['player_lifeform'])
        self.append_result(self.player_info.uid, 'You have sold your {} to {} for {} riphons.'.format(self.args['target'].alias(), self.args['interaction'].main_npc.alias(), price))
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
        del self.args['target'].id

        items = self.args['target'].split(self.args['target'], self.args['quantity'])
        self.args['interaction'].main_npc.inventory.append(items[0])
        if len(items) > 1:
            self.args['player_lifeform'].inventory.append(items[1])

        failure = self.args['target'].on_take(self.args['interaction'].main_npc)
        return failure
