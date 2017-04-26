from erukar import *
import unittest

class UnequipTests(unittest.TestCase):
    def test_unequip_weapon(self):
        p = Player()
        dungeon = Dungeon()
        room = Room(dungeon)
        room.add(p)

        w = Weapon()
        w.name = 'Sword'
        p.inventory.append(w)
        p.right = w

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'equipment_slot': 'right'}
        result = u.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, None)
        self.assertIn('successfully', result.result_for(p.uuid)[0])

    def test_unequip_armor(self):
        p = Player()
        dungeon = Dungeon()
        room = Room(dungeon)
        room.add(p)

        a = Armor()
        a.name = 'Plate Mail'
        p.inventory.append(a)
        p.chest = a

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'equipment_slot': 'chest'}
        result = u.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, None)
        self.assertIn('successfully', result.result_for(p.uuid)[0])

    def test_unequip_armor_without_action_points(self):
        p = Player()
        p.action_points = 0
        dungeon = Dungeon()
        room = Room(dungeon)
        room.add(p)

        a = Armor()
        a.name = 'Plate Mail'
        p.inventory.append(a)
        p.chest = a

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'equipment_slot': 'chest'}
        result = u.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, a)
        self.assertFalse(result.success)

    def test_unequip_item(self):
        p = Player()
        dungeon = Dungeon()
        room = Room(dungeon)
        room.add(p)

        i = Item()
        i.item_type = 'Potion'
        p.inventory.append(i)

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'equipment_slot': 'chest'}
        result = u.execute()

        self.assertTrue(i in p.inventory)
        self.assertFalse(result.success)
