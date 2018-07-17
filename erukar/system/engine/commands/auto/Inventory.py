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
        player = self.args['player_lifeform']
        for item in player.inventory:
            items.append(Inventory.format_item(item, player))
        obj_response = {
            'inventory': items,
            'equipment': list(self.assemble_equipment())
        }
        self.append_result(self.player_info.uid, obj_response)
        return self.succeed()

    def assemble_equipment(self):
        player = self.args['player_lifeform']
        for slot in Inventory.InventorySlots:
            yield Inventory.format_equipment(player, slot)

    def format_equipment(player, slot):
        return {
            'slot': slot,
            'slotName': Inventory.SlotName[slot],
            'id': Inventory.uid_for_slot(player, slot)
        }

    def uid_for_slot(pawn, slot):
        if hasattr(pawn, slot):
            item = getattr(pawn, slot)
            if item:
                return str(item.uuid)
        return -1

    def format_item(item, player):
        object_output = {
            'id': str(item.uuid),
            'alias': item.alias(),
            'quantifiable_alias': item.long_alias(),
            'quantity': getattr(item, 'quantity', 1),
            'price': int(item.price(player.world.economy())),
            'isUsable': item.IsUsable,
            'desirabilityRating': item.rarity().name,
            'slots': item.equipment_slots(player),
            'flavorText': item.flavor_text(player),
            'details': list(Inventory.generate_list_of_details(item))
        }

        if item.material:
            object_output['durability'] = {
                'current': item.durability,
                'max': item.max_durability()
            }

        if isinstance(item, Weapon):
            details = list(Inventory.weapon_details(player, item))
            object_output['damages'] = details

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

    def weapon_details(player, item):
        yield from item.generate_damage_details_for_inventory(player)

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
