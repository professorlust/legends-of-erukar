from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar

class Inventory(Command):
    header = 'INVENTORY\n----------\n{}\n----------\n{}'
    item = "{:10}. {}"

    aliases = ['inventory']

    def execute(self, *_):
        char = self.find_player().character
        # All of the Other items
        items = '\n'.join(Inventory.inventory_contents(char))
        equipment = self.equipment(char)
        self.append_result(self.sender_uid, self.header.format(equipment, items))
        return self.succeed()

    def equipment(self, character):
        '''Draw (Equipped) Equipment'''
        armor_results = []
        for armor_type in Lifeform.equipment_types:
            armor = getattr(character, armor_type)
            armor_name = 'None'
            if armor is not None:
                armor_name = armor.on_inventory_inspect(character)
            armor_results.append(self.item.format(armor_type.capitalize(), armor_name))
        return '\n'.join(armor_results)

    def inventory_contents(character):
        for i, item in enumerate(character.inventory):
            yield '{:2}. {}'.format(i+1, item.on_inventory())

    def get_header(self, char):
        '''Draw Equipment'''
        result = Inventory.header
        descriptions = (self.describe_attribute(char, item_type)\
            for item_type in Lifeform.equipment_types)
        return result.format(*descriptions)

    def describe_attribute(self, character, name):
        result = getattr(character, name)
        if result is not None:
            return result.describe()
