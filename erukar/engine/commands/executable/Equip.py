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
    TrackedParameters = ['equip_location', 'item']

    def execute(self):
        player = self.find_player()
        if player is None: return
        lifeform = player.lifeform()

        payload, target = self.check_for_arguments()

        if not target:
            # Get the item from our inventory if it exists
            item, failure_object = self.find_in_inventory(player, payload)
            if failure_object:
                return failure_object

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

    def check_for_arguments(self):
        payload = self.payload()

        # Check to see if we are disambiguating
        if self.context.requires_disambiguation:
            self.context.resolve_disambiguation(payload)

            # Now copy all of the tracked Params into this command
            self.context.copy_tracked_parameters(self)

            # Check to make sure all tracked parameters are set
            return self.fail_if_requires_disambiguation()

        location_designation, secondary_payload = payload.split(' ', 1)
        location = self.decode_location(location_designation)
        if location:
            self.equip_location = location

    def decode_location(self, location_designation):
        lifeform = self.find_player().lifeform()
        # Check for direct matches
        if location_designation in lifeform.equipment_types:
            return location_designation
        # Check for aliases
        if location_designation in self.equipment_location_codes:
            return self.equipment_location_codes[location_designation]
        return 'err_no_slot'
