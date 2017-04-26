from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon
import re

class Equip(ActionCommand):
    NotFound = "Object cannot be equipped as it was not found"
    CannotEquip = "'{}' was found but cannot be equipped"
    MismatchedSlot = "Cannot equip {} at slot {}"

    '''
    Requires:
        equipment_slot
        inventory_item
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        # Error handling
        if not self.args['inventory_item']: return self.fail(Equip.NotFound)
        if self.args['equipment_slot'] not in self.args['inventory_item'].EquipmentLocations:
            return self.fail(Equip.CannotEquip.format(self.args['inventory_item'].describe()))

        equipment = getattr(self.args['player_lifeform'], self.args['equipment_slot'])
        cost = Equip.get_cost_to_equip(equipment, self.args['inventory_item'])

        if self.args['player_lifeform'].action_points < cost:
            return self.fail('Not enough action points to equip {} to {}'.format(equipment.alias(), self.args['equipment_slot']))
        self.args['player_lifeform'].action_points -= cost

        self.perform_swap(equipment)
        result = '{} equipped as {} successfully.'.format(self.args['inventory_item'].describe(), self.args['equipment_slot'])
        self.append_result(self.player_info.uuid, result)
        return self.succeed()

    def get_cost_to_equip(equipped, to_equip):
        '''Always takes the higher of the unequip and equip AP costs'''
        if not equipped:
            return to_equip.ActionPointCostToEquip
        return max(to_equip.ActionPointCostToEquip, equipped.ActionPointCostToUnequip)

    def perform_swap(self, equipment):
        setattr(self.args['player_lifeform'], self.args['equipment_slot'], self.args['inventory_item'])
        self.dirty(self.args['player_lifeform'])

        # Unequip
        if equipment:
            result = equipment.on_unequip(self.args['player_lifeform'])
            if result: self.append_result(self.player_info.uuid, result)

        # Equip new item
        effects = self.args['inventory_item'].on_equip(self.args['player_lifeform'])
        if effects: self.append_result(self.player_info.uuid, effects)
