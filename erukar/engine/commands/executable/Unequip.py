from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon

class Unequip(ActionCommand):
    not_found = "No equipped item '{0}' was found"
    aliases = ['unequip']

    def execute(self):
        lifeform = self.find_player().lifeform()
        payload = self.check_for_arguments()

        # Figure out the item type
        item_type = self.determine_type(lifeform, payload)

        # remove if we know the type
        if item_type is not '':
            item = getattr(lifeform, item_type)
            setattr(lifeform, item_type, None)
            item.on_unequip(lifeform)
            results = '{} unequipped from {} successfully.'.format(item.describe(), item_type)
            self.dirty(lifeform)
            self.append_result(self.sender_uid, results)
            return self.succeed()

        # Nothing was found
        results = Unequip.not_found.format(payload)
        return self.fail(results)

    def determine_type(self, lifeform, payload):
        if payload in Lifeform.equipment_types:
            return payload
        for e_type in Lifeform.equipment_types:
            equipped = getattr(lifeform, e_type)
            if equipped is not None:
                if payload.lower() in equipped.describe().lower():
                     return e_type
        return ''

    def check_for_arguments(self):
        payload = self.payload()
        args = payload.split(' ', 1)
        self.arguments['hand'] = 'right'
        if len(args) > 1:
            if args[0] in ['left', 'off', 'offhand']:
                self.arguments['hand'] = 'left'
                return args[1]
        return payload
