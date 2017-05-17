from erukar import *
import unittest

class UnequipTests(unittest.TestCase):
    def test_unequip_weapon(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 2
        room = Room(dungeon, [(0,1)])
        room.add(p)

        w = Weapon()
        w.name = 'Sword'
        p.inventory.append(w)
        p.right = w

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'inventory_item': str(w.uuid)}
        result = u.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, None)
        self.assertTrue(result.success)

    def test_unequip_armor(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 2
        room = Room(dungeon, [(0,1)])
        room.add(p)

        a = Armor()
        a.name = 'Plate Mail'
        p.inventory.append(a)
        p.chest = a

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'inventory_item': str(a.uuid)}
        result = u.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, None)
        self.assertTrue(result.success)

    def test_unequip_armor_without_action_points(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 0
        room = Room(dungeon, [(0,1)])
        room.add(p)

        a = Armor()
        a.name = 'Plate Mail'
        p.inventory.append(a)
        p.chest = a

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'inventory_item': str(a.uuid)}
        result = u.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, a)
        self.assertFalse(result.success)

    def test_unequip_item(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 2
        room = Room(dungeon, [(0,1)])
        room.add(p)

        i = Item()
        i.item_type = 'Potion'
        p.inventory.append(i)

        u = Unequip()
        u.world = dungeon
        u.player_info = p
        u.args = {'inventory_item': str(i.uuid)}
        result = u.execute()

        self.assertTrue(i in p.inventory)
        self.assertFalse(result.success)
