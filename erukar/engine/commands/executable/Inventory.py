from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar, json

class Inventory(Command):
    def perform(self):
        pass

    def format_item_json(item):
        return json.dumps({
            'id': str(item.uuid),
            'alias': item.alias(),
            'durability': {'current': item.durability(), 'max': item.max_durability()},
            'desirabilityRating': item.rarity(),
            'slots': item.EquipmentLocations,
            'details': list(Inventory.generate_list_of_details(item)) #[
#               {type: 'property', title: '', value: '3 to 4 Slashing Damage'},
#               {type: 'standard', title: 'Weight', value: '10.50 levts'},
#               {type: 'standard', title: 'Iron', value: 'A strong base metal -- hard to forge and fairly heavy but resilient'},
#               {type: 'legendary', title: 'Legendary Magekiller', value: 'Has a 25% chance to burst stored hexcells'},
#               {type: 'description', title: '', value: 'The pole of Ankithalis is a carved Iurwood reinforced with rings of platinum and adorned by sapphires. In its entirety, Ankithalis is roughly 6 feet and 3 inches long. The head of the halberd bears the insignia of King Tyroche Alar of Iuria, the Renegade King. Various symbols describe how Browr Trowr, Galadrast advocate of King Alar, used the weapon in defense of his liege.'}
           #]
        })

    def generate_list_of_details(item):
        yield Inventory.format_modifier(item.material)
        for modifier in item.modifiers:
            yield Inventory.format_modifier(modifier)

    def format_modifier(modifier):
        return {
            'type': modifier.rarity().name,
            'title': modifier.InventoryName,
            'value': modifier.InventoryDescription
        }
            
