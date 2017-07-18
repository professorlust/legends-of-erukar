from erukar.engine.commands.Command import SearchScope
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon
import re

class Equip(ActionCommand):
    NotFound = "Object cannot be equipped as it was not found"
    CannotEquip = "'{}' was found but cannot be equipped"
    MismatchedSlot = "Cannot equip {} at slot {}"
    NotEnoughPoints = 'Not enough action points to equip {} to {}'
    RebuildZonesOnSuccess = True

    '''
    Requires:
        equipment_slot
        interaction_target
    '''
    def __init__(self):
        super().__init__()
        self.search_scope = SearchScope.Inventory

    def perform(self):
        # Error handling
        if not self.args['interaction_target']: return self.fail(Equip.NotFound)
        if self.args['equipment_slot'] not in self.args['interaction_target'].EquipmentLocations:
            return self.fail(Equip.CannotEquip.format(self.args['interaction_target'].describe()))

        if self.args['equipment_slot'] in ['left', 'right']:
            left = self.args['player_lifeform'].left
            right = self.args['player_lifeform'].right
            if (left and left.RequiresTwoHands) or (right and right.RequiresTwoHands):
                return self.equip_on_two_handed()

        return self.equip_in_place()

    def equip_on_two_handed(self):
        '''occurs when we're equipping an item that needs two hands'''
        two_handed_slot = next(slot for slot in ['left','right'] if getattr(self.args['player_lifeform'], slot))
        equipment = getattr(self.args['player_lifeform'], two_handed_slot)

        err = self.check_cost(equipment)
        if err: return err

        self.remove_equipment(equipment, two_handed_slot)
        setattr(self.args['player_lifeform'], self.args['equipment_slot'], self.args['interaction_target'])
        result = '{} equipped as {} successfully.'.format(self.args['interaction_target'].describe(), self.args['equipment_slot'])
        self.append_result(self.player_info.uid, result)
        return self.succeed()

    def equip_in_place(self):
        '''Used when we're not equipping on top of a two-handed item'''
        equipment = getattr(self.args['player_lifeform'], self.args['equipment_slot'])
        err = self.check_cost(equipment)
        if err: return err

        self.perform_swap(equipment)
        result = '{} equipped as {} successfully.'.format(self.args['interaction_target'].describe(), self.args['equipment_slot'])
        self.append_result(self.player_info.uid, result)
        return self.succeed()

    def check_cost(self, equipment):
        cost = self.cost_to_equip(equipment, self.args['interaction_target'])
        if self.args['player_lifeform'].action_points() < cost:
            return self.fail(Equip.NotEnoughPoints.format(equipment.describe(), self.args['equipment_slot']))
        self.args['player_lifeform'].consume_action_points(cost)

    def cost_to_equip(self, equipped, to_equip):
        '''Always takes the higher of the unequip and equip AP costs'''
        if not equipped:
            return to_equip.ActionPointCostToEquip

        if self.args['interaction_target'].RequiresTwoHands:
            ap_costs = [
                0 if not self.args['player_lifeform'].left  else self.args['player_lifeform'].left.ActionPointCostToUnequip,
                0 if not self.args['player_lifeform'].right else self.args['player_lifeform'].right.ActionPointCostToUnequip,
                to_equip.ActionPointCostToEquip
            ]
            return max(ap_costs)

        return max(to_equip.ActionPointCostToEquip, equipped.ActionPointCostToUnequip)

    def perform_swap(self, equipment):
        if isinstance(self.args['interaction_target'], Weapon) and self.args['interaction_target'].RequiresTwoHands:
            self.swap_two_handed()
        else: self.remove_equipment(equipment, self.args['equipment_slot'])

        setattr(self.args['player_lifeform'], self.args['equipment_slot'], self.args['interaction_target'])
        self.dirty(self.args['player_lifeform'])

        # Equip new item
        effects = self.args['interaction_target'].on_equip(self.args['player_lifeform'])
        if effects: self.append_result(self.player_info.uid, effects)

    def swap_two_handed(self):
        for hand in ['left', 'right']:
            self.remove_equipment(getattr(self.args['player_lifeform'], hand), hand)

    def remove_equipment(self, equipment, eq_slot):
        setattr(self.args['player_lifeform'], eq_slot, None)
        if equipment:
            result = equipment.on_unequip(self.args['player_lifeform'])
            if result: self.append_result(self.player_info.uid, result)
