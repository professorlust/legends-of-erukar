from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar, json

class Inventory(Command):
    NeedsArgs = False

    def perform(self):
        items = []
        for item in self.args['player_lifeform'].inventory:
            items.append(Inventory.format_item(item))
        equipment = [
            { 'slot': 'left', 'slotName': 'Left Hand', 'id': -1 },
            { 'slot': 'right', 'slotName': 'Right Hand', 'id': -1 },
            { 'slot': 'head', 'slotName': 'Head', 'id': -1 },
            { 'slot': 'chest', 'slotName': 'Chest', 'id': -1 },
            { 'slot': 'hands', 'slotName': 'Hands', 'id': -1 },
            { 'slot': 'legs', 'slotName': 'Legs', 'id': -1 },
            { 'slot': 'feet', 'slotName': 'Feet', 'id': -1 },
            { 'slot': 'left_ring', 'slotName': 'Left Ring', 'id': -1 },
            { 'slot': 'right_ring', 'slotName': 'Right Ring', 'id': -1 },
            { 'slot': 'ammunition', 'slotName': 'Ammunition', 'id': -1 },
            { 'slot': 'blessing', 'slotName': 'Blessing', 'id': -1 },
        ]
        obj_response = {
            'inventory': items,
            'equipment': equipment
        }
        self.append_result(self.player_info.uuid, obj_response)
        return self.succeed()

    def format_item(item):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'desirabilityRating': item.rarity(),
            'slots': item.EquipmentLocations,
            'details': list(Inventory.generate_list_of_details(item)) 
        }

        if item.material:
            object_output['durability'] = {'current': item.durability(), 'max': item.max_durability()}

        if isinstance(item, erukar.engine.inventory.Weapon):
            object_output['damage'] = {}
            for name, d_range in Inventory.weapon_details(item):
                object_output['damage'][name] = d_range

        if isinstance(item, erukar.engine.inventory.Armor):
            object_output['protection'] = {}
            for name, mit in Inventory.armor_details(item):
                object_output['protection'][name] = mit

        return object_output

    def generate_list_of_details(item):
        if item.material:
            yield Inventory.format_modifier(item.material)
        for modifier in item.modifiers:
            yield Inventory.format_modifier(modifier)
        # Description here

    def weapon_details(item):
        for damage in item.damages:
            yield damage.name.capitalize(), '{} to {}'.format(damage.damage[0], damage.damage[1])

    def armor_details(item):
        for mit in item.DamageMitigations:
            yield mit.capitalize(), {'deflection': item.DamageMitigations[mit][1], 'mitigation': item.DamageMitigations[mit][0]}

    def format_modifier(modifier):
        return {
            'type': modifier.rarity().name,
            'title': modifier.InventoryName,
            'value': modifier.InventoryDescription
        }
            
