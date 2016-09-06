from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar

class Inventory(Command):
    header = 'INVENTORY\n----------\n{}\n----------\n{}'
    item = "{:10}. {}"

    def execute(self, *_):
        char = self.find_player().character

        items = '\n'.join(['{:2}. {}'.format(i, char.inventory[i].on_inventory())\
            for i in range(0, len(char.inventory))])
        equipment = self.equipment(char)
        return self.succeed(self.header.format(equipment, items))

    def equipment(self, character):
        armor_results = []
        for armor_type in Lifeform.equipment_types:
            armor = getattr(character, armor_type)
            armor_name = 'None'
            if armor is not None:
                armor_name = armor.on_inventory()
            armor_results.append(self.item.format(armor_type.capitalize(), armor_name))
        return '\n'.join(armor_results)

    def get_header(self, char):
        result = Inventory.header
        descriptions = (self.describe_attribute(char, item_type)\
            for item_type in Lifeform.equipment_types)
        return result.format(*descriptions)

    def describe_attribute(self, character, name):
        result = getattr(character, name)
        if result is not None:
            return result.describe()
