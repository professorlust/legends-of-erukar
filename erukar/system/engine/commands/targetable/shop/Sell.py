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

        if self.args['interaction'].main_npc.wealth > self.args['target'].price():
            return self.do_sell()

        return self.fail('NPC cannot buy your {}'.format(self.args['target'].alias()))

    def do_sell(self):
        price = self.args['target'].price()
        self.args['player_lifeform'].wealth += price
        self.args['player_lifeform'].inventory.remove(self.args['target'])
        equipment_slot = self.get_equip_slot()
        if equipment_slot:
            setattr(self.args['player_lifeform'], equipment_slot, None)

        self.args['interaction'].main_npc.wealth -= price
        self.args['interaction'].main_npc.inventory.append(self.args['target'])
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
