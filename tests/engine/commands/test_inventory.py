from erukar import *
import unittest, erukar

class InventoryTests(unittest.TestCase):
    def test_format_weapon_json(self):
        item = Sword()
        erukar.game.modifiers.material.Steel().apply_to(item)
        result = Inventory.format_item(item)

        self.assertEqual(result['id'], str(item.uuid))
        self.assertIn('Slashing', result['damages'])

    def test_format_armor_json(self):
        item = Hauberk()
        erukar.game.modifiers.material.Steel().apply_to(item)
        result = Inventory.format_item(item)

        self.assertEqual(result['id'], str(item.uuid))
        self.assertIn('Slashing', result['protection'])

    def test_inventory_execute(self):
        p = Player()
        d = Dungeon()

        h = Hauberk()
        s = Sword()
        erukar.game.modifiers.material.Steel().apply_to(h)
        erukar.game.modifiers.material.Steel().apply_to(s)
        p.inventory.append(h)
        p.inventory.append(s)

        cmd = Inventory()
        cmd.world = d
        cmd.player_info = p
        result = cmd.execute() 

        self.assertTrue(result.success)
        self.assertEqual(len(result.result_for(p.uuid)[0]['inventory']), 2)

    def test_format_armor_potion(self):
        item = Potion()
        result = Inventory.format_item(item)
        self.assertTrue(True)

    def test_format_modifier(self):
        modifier = Modifier()
        modifier.rarity = erukar.engine.model.enum.Rarity.Legendary
        modifier.InventoryName = 'Injected Test Name'
        modifier.InventoryDescription = 'Injected Test Description'

        result = Inventory.format_modifier(modifier)

        self.assertEqual(result['type'], 'Legendary')
        self.assertEqual(result['title'], 'Injected Test Name')
        self.assertEqual(result['value'], 'Injected Test Description')
