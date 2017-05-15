from erukar import *
import unittest

class EquipTests(unittest.TestCase):
    def test_cost_to_equip(self):
        a = Armor('')
        a.ActionPointCostToUnequip = 1
        b = Armor('')
        b.ActionPointCostToEquip = 2

        e = Equip()
        e.args = {'interaction_target': a}
        result = e.cost_to_equip(a,b)
        self.assertEqual(result, 2)

    def test_equip_weapon(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        w = Weapon()
        p.inventory.append(w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'right', 'interaction_target': w.uuid}
        result = e.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, w)
        self.assertTrue(result.success)

    def test_equip_weapon_two_handed(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        p.right = Weapon()
        p.left = Shield('')

        w = Weapon()
        w.RequiresTwoHands = True
        p.inventory.append(w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'right', 'interaction_target': w.uuid}
        result = e.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, w)
        self.assertEqual(p.left, None)
        self.assertTrue(result.success)

    def test_equip_when_two_handed_equipped_not_enough_ap(self):
        p = Player()
        dungeon = Dungeon()

        w = Weapon()
        w.RequiresTwoHands = True
        p.inventory.append(w)
        p.right = w

        new_w = Weapon()
        p.inventory.append(new_w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'left', 'interaction_target': new_w.uuid}
        result = e.execute()

        self.assertEqual(p.left, None)
        self.assertEqual(p.right, w)
        self.assertFalse(result.success)

    def test_equip_when_two_handed_equipped_same_slot(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        w = Weapon()
        w.RequiresTwoHands = True
        p.inventory.append(w)
        p.right = w

        new_w = Weapon()
        p.inventory.append(new_w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'right', 'interaction_target': new_w.uuid}
        result = e.execute()

        self.assertEqual(p.left, None)
        self.assertEqual(p.right, new_w)
        self.assertTrue(result.success)

    def test_equip_when_two_handed_equipped_different_slot(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        w = Weapon()
        w.RequiresTwoHands = True
        p.inventory.append(w)
        p.left = w

        new_w = Weapon()
        p.inventory.append(new_w)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'right', 'interaction_target': new_w.uuid}
        result = e.execute()

        self.assertEqual(p.left, None)
        self.assertEqual(p.right, new_w)
        self.assertTrue(result.success)

    def test_equip_armor(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        a = Armor('')
        p.inventory.append(a)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'chest', 'interaction_target': a.uuid}
        result = e.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, a)
        self.assertTrue(result.success)

    def test_equip_item(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        i = Item('Potion', 'Potion')
        p.inventory.append(i)

        e = Equip()
        e.world = dungeon
        e.player_info = p
        e.args = {'equipment_slot': 'chest', 'interaction_target': i.uuid}
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.chest, i)
        self.assertNotEqual(p.right, i)
        self.assertFalse(result.success)
