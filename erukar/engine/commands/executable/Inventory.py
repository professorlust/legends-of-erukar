from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms.Lifeform import Lifeform
import erukar, json

class Inventory(Command):
    NeedsArgs = False
    InventorySlots = [
        "left",
        "right",
        "chest",
        "head",
        "feet",
        "arms",
        "legs",
        "ring",
        "amulet",
        "blessing",
        "ammunition",
    ]
    SlotName = {
        'left': 'Left Hand',
        'right': 'Right Hand',
        'head': 'Head',
        'chest': 'Chest',
        'arms': 'Arms',
        'legs': 'Legs',
        'feet': 'Feet',
        'ring': 'Ring',
        'amulet': 'Amulet',
        'blessing': 'Blessing',
        'ammunition': 'Ammunition',
    }

    def perform(self):
        items = []
        for item in self.args['player_lifeform'].inventory:
            items.append(Inventory.format_item(item))
        obj_response = {
            'inventory': items,
            'equipment': list(self.assemble_equipment())
        }
        self.append_result(self.player_info.uid, obj_response)
        return self.succeed()

    def assemble_equipment(self):
        for slot in Inventory.InventorySlots:
            yield {
                'slot': slot,
                'slotName': Inventory.SlotName[slot],
                'id': Inventory.uid_for_slot(self.args['player_lifeform'], slot)
            }

    def uid_for_slot(pawn, slot):
        if hasattr(pawn, slot):
            item = getattr(pawn, slot)
            if item: return str(item.uuid)
        return -1

    def format_item(item):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'desirabilityRating': item.rarity().name,
            'slots': item.EquipmentLocations,
            'details': list(Inventory.generate_list_of_details(item)) 
        }

        if item.material:
            object_output['durability'] = {'current': item.durability(), 'max': item.max_durability()}

        if isinstance(item, erukar.engine.inventory.Weapon):
            object_output['damages'] = {}
            for name, d_range in Inventory.weapon_details(item):
                object_output['damages'][name] = d_range

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
            'type': modifier.rarity.name,
            'title': modifier.InventoryName,
            'value': modifier.InventoryDescription
        }
            
