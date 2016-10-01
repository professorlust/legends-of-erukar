from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon
import re

class Equip(ActionCommand):
    not_found = "Unable to find '{0}' in inventory"
    cannot_equip = "'{}' was found but cannot be equipped"

    aliases = ['equip']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()

        payload = self.check_for_arguments()

        # Get the item from our inventory if it exists
        item = self.find_in_inventory(player, payload)
        if item is None:
            return self.fail(Equip.not_found.format(payload))

        # Check to see if the item's type exists as a field on the character
        item_type = self.determine_type(item, lifeform)
        if hasattr(lifeform, item_type):
            setattr(lifeform, item_type, item)
            item.on_equip(lifeform)
            self.dirty(lifeform)
            result = '{} equipped as {} successfully.'.format(item.describe(), item_type)
            self.append_result(self.sender_uid, result)
            return self.succeed()

        return self.fail(Equip.cannot_equip.format(item.describe()))

    def determine_type(self, item, lifeform):
        '''
        This determines what equipment slot should be evaluated; prior to this, it
        is assumed that check_for_arguments has been called to determine which hand
        to assign to.
        '''
        if item.belongs_in_hand(lifeform):
            return self.arguments['hand']
        if len(item.EquipmentLocations) > 0:
            return item.EquipmentLocations[0]
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
