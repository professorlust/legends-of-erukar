from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon

class Unequip(ActionCommand):
    not_found = "No equipped item '{0}' was found"
    unequipped_right = "'{}' unequipped from primary hand weapon successfully"
    unequipped_left = "'{}' unequipped from off hand successfully"
    unequipped_chest = "'{}' unequipped from chest armor successfully"
    unequipped_helm = "'{}' unequipped from helm successfully"
    unequipped_gloves = "'{}' unequipped from gloves successfully"
    unequipped_pants = "'{}' unequipped from pants successfully"
    unequipped_boots = "'{}' unequipped from boots successfully"
    unequipped_ring = "'{}' unequipped from ring successfully"
    unequipped_amulet = "'{}' unequipped from amulet successfully"
    unequipped_blessing = "'{}' unequipped from blessing successfully"

    def execute(self):
        player = self.find_player()
        if player is None: return

        lifeform = self.lifeform(player)
        self.check_for_arguments()

        # Figure out the item type
        item_type = self.determine_type(lifeform)

        # remove if we know the type
        if item_type is not '':
            item = getattr(lifeform, item_type)
            setattr(lifeform, item_type, None)
            uneq_string = getattr(self, 'unequipped_{}'.format(item_type))
            return uneq_string.format(item.describe())

        # Nothing was found
        return Unequip.not_found.format(self.payload)

    def determine_type(self, lifeform):
        if self.payload in Lifeform.equipment_types:
            return self.payload
        for e_type in Lifeform.equipment_types:
            equipped = getattr(lifeform, e_type)
            if equipped is not None:
                if self.payload.lower() in equipped.describe().lower():
                     return e_type
        return ''

    def check_for_arguments(self):
        args = self.payload.split(' ', 1)
        self.arguments['hand'] = 'right'
        if len(args) > 1:
            if args[0] in ['left', 'off', 'offhand']:
                self.arguments['hand'] = 'left'
                self.payload = args[1]
