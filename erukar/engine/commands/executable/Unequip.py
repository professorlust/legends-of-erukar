from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.inventory.Armor import Armor
from erukar.engine.inventory.Weapon import Weapon

class Unequip(ActionCommand):
    not_found = "No equipped item '{0}' was found"

    TrackedParameters = ['item_or_type']
    aliases = ['unequip']

    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        if isinstance(self.item_or_type, str):
            item = getattr(self.lifeform, self.item_or_type)
            location = self.item_or_type
        else:
            item = self.item_or_type
            location = next((loc for loc in self.lifeform.equipment_types 
                            if getattr(self.lifeform, loc) is item), None)
            if not location:
                return self.fail('Could not find location for type')


        if item is None:
            return self.fail('Nothing was found equipped at {}.'.format(location))
        setattr(self.lifeform, location, None)
        item.on_unequip(self.lifeform)
        results = '{} unequipped from {} successfully.'.format(item.describe(), location)
        self.dirty(self.lifeform)
        self.append_result(self.sender_uid, results)
        return self.succeed()

    def resolve_item_or_type(self, opt_payload=''):
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self):
            self.item_or_type = getattr(self.context, 'item_or_type')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'item_or_type') and self.item_or_type: return

        # Combine the Lifeform Equipment Types with Inventory
        inventory_dict = {item.alias(): item for item in self.lifeform.inventory}
        equipment_type_dict = {eqt: eqt for eqt in self.lifeform.equipment_types}
        equipment_type_dict.update(inventory_dict)

        return self.find_in_dictionary(opt_payload, equipment_type_dict, 'item_or_type')
