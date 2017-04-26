from erukar import *
import unittest

class EquipTests(unittest.TestCase):
    def test_cost_to_equip(self):
        a = Armor('')
        a.ActionPointCostToUnequip = 1
        b = Armor('')
        b.ActionPointCostToEquip = 2

        result = Equip.get_cost_to_equip(a,b)
        self.assertEqual(result, 2)

    def test_equip_weapon(self):
        p = Player()
        dungeon = Dungeon()

        w = Weapon()
        p.inventory.append(w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'right', 'inventory_item': w.uuid}
        result = e.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, w)
        self.assertTrue(result.success)

    def test_equip_armor(self):
        p = Player()
        dungeon = Dungeon()

        a = Armor('')
        p.inventory.append(a)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'chest', 'inventory_item': a.uuid}
        result = e.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, a)
        self.assertTrue(result.success)

    def test_equip_item(self):
        p = Player()
        dungeon = Dungeon()

        i = Item('Potion', 'Potion')
        p.inventory.append(i)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'chest', 'inventory_item': i.uuid}
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.chest, i)
        self.assertNotEqual(p.right, i)
        self.assertFalse(result.success)
