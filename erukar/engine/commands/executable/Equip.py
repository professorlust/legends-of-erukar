from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon
import re

class Equip(ActionCommand):
    not_found = "Unable to find '{0}' in inventory"
    equipped_right = "'{}' equipped as primary hand weapon successfully"
    equipped_left = "'{}' equipped in off hand successfully"
    equipped_chest = "'{}' equipped as chest armor successfully"
    equipped_head = "'{}' equipped as helm successfully"
    equipped_arms = "'{}' equipped as gloves successfully"
    equipped_legs = "'{}' equipped as pants successfully"
    equipped_feet = "'{}' equipped as boots successfully"
    equipped_ring = "'{}' equipped as ring successfully"
    equipped_amulet = "'{}' equipped as amulet successfully"
    equipped_blessing = "'{}' equipped as blessing successfully"
    cannot_equip = "'{}' was found but cannot be equipped"

    aliases = ['equip']

    def execute(self):
        player = self.find_player()
        if player is None: return

        payload = self.check_for_arguments()

        # Get the item from our inventory if it exists
        item = self.find_in_inventory(player, payload)
        if item is None:
            return self.fail(Equip.not_found.format(payload))

        # Check to see if the item's type exists as a field on the character
        item_type = self.determine_type(item)
        if hasattr(player.lifeform(), item_type):
            setattr(player.lifeform(), item_type, item)
            result_string_format = getattr(Equip, 'equipped_{0}'.format(item_type))
            self.dirty(player.lifeform())
            return self.succeed(result_string_format.format(item.describe()))

        return self.fail(Equip.cannot_equip.format(item.describe()))

    def determine_type(self, item):
        '''
        This determines what equipment slot should be evaluated; prior to this, it
        is assumed that check_for_arguments has been called to determine which hand
        to assign to.
        '''
        if item.belongs_in_hand():
            return self.arguments['hand']
        if len(item.equipment_locations) > 0:
            return item.equipment_locations[0]
        return 'error_no_equip_slot'

    def check_for_arguments(self):
        payload = self.payload()
        args = payload.split(' ', 1)
        self.arguments['hand'] = 'right'
        if len(args) <= 1:
            return args[0]

        if args[0] in ['left', 'off', 'offhand']:
            self.arguments['hand'] = 'left'
            return args[1]

        if args[0] in ['right', 'main', 'primary']:
            return args[1]

        return payload
