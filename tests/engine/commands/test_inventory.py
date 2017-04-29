from erukar import *
import unittest, erukar

class InventoryTests(unittest.TestCase):
    def test_format_item_json(self):
        item = Sword()
        erukar.game.modifiers.material.Steel().apply_to(item)
        result = Inventory.format_item_json(item)
        print(result)

        self.assertIn(str(item.uuid), result)
