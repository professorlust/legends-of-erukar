from erukar.system.engine import Weapon, Armor
from ..Command import Command


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
        lifeform = self.args['player_lifeform']
        for slot in Inventory.InventorySlots:
            yield {
                'slot': slot,
                'slotName': Inventory.SlotName[slot],
                'id': Inventory.uid_for_slot(lifeform, slot)
            }

    def uid_for_slot(pawn, slot):
        if hasattr(pawn, slot):
            item = getattr(pawn, slot)
            if item:
                return str(item.uuid)
        return -1

    def format_item(self, item):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'quantifiable_alias': item.long_alias(),
            'quantity': getattr(item, 'quantity', 1),
            'price': int(item.price(self.world.economy())),
            'isUsable': item.IsUsable,
            'desirabilityRating': item.rarity().name,
            'slots': item.equipment_slots(self.args['player_lifeform']),
            'flavorText': item.flavor_text(self.args['player_lifeform']),
            'details': list(Inventory.generate_list_of_details(item))
        }

        if item.material:
            object_output['durability'] = {
                'current': item.durability,
                'max': item.max_durability()
            }

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
        lifeform = self.args['player_lifeform']
        yield from item.generate_damage_details_for_inventory(lifeform)

    def armor_details(item):
        for mit in item.DamageMitigations:
            yield mit.capitalize(), {
                'deflection': item.DamageMitigations[mit][1],
                'mitigation': item.DamageMitigations[mit][0]
            }

    def format_modifier(modifier):
        return {
            'type': modifier.rarity.name,
            'title': modifier.InventoryName,
            'value': modifier.InventoryDescription
        }
