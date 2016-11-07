from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon
import re

class Equip(ActionCommand):
    not_found = "Unable to find '{0}' in inventory"
    cannot_equip = "'{}' was found but cannot be equipped"

    equipment_location_codes = {
        'off': 'left',
        'offhand': 'left',
        'main': 'right',
        'primary': 'right'
    }
    aliases = ['equip']
    TrackedParameters = ['item','equip_location']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()

        failure = self.check_for_arguments()
        if failure:
            return failure

        # Check to see if the item's type exists as a field on the character
        if hasattr(lifeform, self.equip_location):
            setattr(lifeform, self.equip_location, self.item)
            self.item.on_equip(lifeform)
            self.dirty(lifeform)
            result = '{} equipped as {} successfully.'.format(self.item.describe(), self.equip_location)
            self.append_result(self.sender_uid, result)
            return self.succeed()

        return self.fail(Equip.cannot_equip.format(self.item.describe()))

    def resolve_item(self, opt_payload=''):
        player = self.find_player().lifeform()
        self.item = self.context.item if self.context else None
        if self.item:
            return

        if opt_payload:
            payload = opt_payload.split(' ', 1)
            if len(payload) > 1:
                first_arg_is_valid_location = not self.resolve_equip_location(payload[0])
                if first_arg_is_valid_location:
                    payload.pop(0)

        return self.find_in_inventory(player, payload[0], 'item')

    def resolve_equip_location(self, opt_payload=''):
        self.equip_location = self.context.equip_location if self.context else None
        if self.equip_location:
            return

        if self.item:
            return self.post_process_search(self.item.EquipmentLocations, 'Equipment Location', 'equip_location')

        if opt_payload:
            decoded = self.decode_location(opt_payload)
            if decoded:
                self.equip_location = decoded
                return

        return self.fail('Nothing can be done for equip_location')

    def process_input_payload(self, payload):
        '''Figure out the location and inventory type'''
        print('processing input payload')
        player = self.find_player().lifeform()
        split_parameters = payload.split(' ', 1)

        # Try to find the location via decoding on the first split if it exists... otherwise ignore
        self.equip_location = self.decode_location(split_parameters[0]) if len(split_parameters) > 1 else ''

        # If location was not the first parameter, the whole payload represents the item alias
        item_name = split_parameters[1] if self.equip_location else payload

        # Now try to find the item in the player's inventory
        failure = self.find_in_inventory(player, item_name, 'item')
        if failure: return failure

        # If we still haven't found the location, grab it from the item

    def decode_location(self, location_designation):
        lifeform = self.find_player().lifeform()
        # Check for direct matches
        if location_designation in lifeform.equipment_types:
            return location_designation
        # Check for aliases
        if location_designation in self.equipment_location_codes:
            return self.equipment_location_codes[location_designation]
        return
