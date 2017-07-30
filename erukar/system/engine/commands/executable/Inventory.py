from erukar.system.engine import Lifeform, Weapon, Armor
from ..Command import Command
import json

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
            items.append(self.format_item(item))
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

    def format_item(self, item):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'desirabilityRating': item.rarity().name,
            'slots': item.equipment_slots(self.args['player_lifeform']),
            'details': list(Inventory.generate_list_of_details(item)) 
        }

        if item.material:
            object_output['durability'] = {'current': item.durability(), 'max': item.max_durability()}

        if isinstance(item, Weapon):
            object_output['damages'] = list(self.weapon_details(item))

        if isinstance(item, Armor):
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

    def weapon_details(self, item):
        for damage in item.damages:
            yield {
                'name': damage.name.capitalize(),
                'range': '{} to {}'.format(*damage.scaled_values(self.args['player_lifeform'])),
                'scaling': '{} x{:.2f} [{},{}]'.format(damage.modifier[:3].upper(), damage.scalar, damage.requirement, damage.max_scale)
            }

    def armor_details(item):
        for mit in item.DamageMitigations:
            yield mit.capitalize(), {'deflection': item.DamageMitigations[mit][1], 'mitigation': item.DamageMitigations[mit][0]}

    def format_modifier(modifier):
        return {
            'type': modifier.rarity.name,
            'title': modifier.InventoryName,
            'value': modifier.InventoryDescription
        }
            
