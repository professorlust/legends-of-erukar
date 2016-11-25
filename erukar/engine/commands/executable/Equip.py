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
        failure = self.check_for_arguments()
        if failure: return failure

        # Check to see if the item's type exists as a field on the character
        if hasattr(self.lifeform, self.equip_location):
            setattr(self.lifeform, self.equip_location, self.item)
            effects = self.item.on_equip(self.lifeform)
            self.dirty(self.lifeform)
            result = '{} equipped as {} successfully.'.format(self.item.describe(), self.equip_location)
            self.append_result(self.sender_uid, result)
            return self.succeed()

        return self.fail(Equip.cannot_equip.format(self.item.describe()))

    def resolve_equip_location(self, opt_payload=''):
        if self.context and self.context.should_resolve(self):
            self.equip_location = getattr(self.context, 'equip_location')

        if hasattr(self, 'equip_location') and self.equip_location: 
            return

        if hasattr(self, 'item') and self.item:
            locations = {i.capitalize(): i for i in self.item.EquipmentLocations}
            return self.find_in_dictionary(opt_payload, locations, 'equip_location')

        if opt_payload:
            decoded = self.decode_location(opt_payload)
            if decoded:
                self.equip_location = decoded
                return

        return self.fail('Nothing can be done for equip_location')

    def check_for_arguments(self):
        # Copy all of the tracked Params into this command
        payload = self.user_specified_payload
        self.payloads = None

        self.player = self.find_player()
        self.lifeform = self.player.lifeform()

        if self.context and self.context.requires_disambiguation and payload.isdigit():
            self.context.resolve_disambiguation(self.context.indexed_items[int(payload)-1])

        if self.context and hasattr(self.context.context, 'payloads') and self.context.context.payloads and self.context.indexed_items:
            self.payloads = getattr(self.context.context, 'payloads')

        if not self.payloads:
            if ' on ' in payload:
                self.payloads = payload.split(' on ', 1)
            else:
                self.payloads = (payload, '')

        fail = self.resolve_item(self.payloads[0])
        if fail: return fail

        fail = self.resolve_equip_location(self.payloads[1])
        if fail: return fail

    def decode_location(self, location_designation):
        '''Attempt to find the location, first by matching, then by aliasing'''
        lifeform = self.find_player().lifeform()
        # Check for direct matches
        if location_designation in lifeform.equipment_types:
            return location_designation
        # Check for aliases
        if location_designation in self.equipment_location_codes:
            return self.equipment_location_codes[location_designation]
        return
