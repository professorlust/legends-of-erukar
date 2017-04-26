from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.commands.ActionCommand import ActionCommand

class Unequip(ActionCommand):
    NotFound = "No equipped item '{0}' was found"

    '''
    Requires:
        equipment_slot
    '''

    def perform(self):
        equipment = getattr(self.args['player_lifeform'], self.args['equipment_slot'])
        if not equipment:
            return self.fail(Unequip.NotFound.format(self.args['equipment_slot']))
        if self.args['player_lifeform'].action_points < equipment.ActionPointCostToUnequip:
            return self.fail('Not enough action points to unequip {} from {}'.format(equipment.alias(), self.args['equipment_slot']))
            
        self.args['player_lifeform'].action_points -= equipment.ActionPointCostToUnequip
        setattr(self.args['player_lifeform'], self.args['equipment_slot'], None)
        result = equipment.on_unequip(self.args['player_lifeform'])
        if result: self.append_result(self.player_info.uuid, result)

        self.dirty(self.args['player_lifeform'])
        result = '{} unequipped from {} successfully.'.format(equipment.describe(), self.args['equipment_slot'])
        self.append_result(self.player_info.uuid, result)
        return self.succeed()
