from erukar import *
import unittest, erukar

class InventoryTests(unittest.TestCase):
    def test_format_weapon_json(self):
        item = Sword()
        erukar.game.modifiers.material.Steel().apply_to(item)
        result = Inventory.format_item_json(item)

        self.assertIn(str(item.uuid), result)
        self.assertIn('Slashing', result)

    def test_format_armor_json(self):
        item = Hauberk()
        erukar.game.modifiers.material.Steel().apply_to(item)
        result = Inventory.format_item_json(item)

        self.assertIn(str(item.uuid), result)
        self.assertIn('Slashing', result)
