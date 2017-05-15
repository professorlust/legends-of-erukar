from erukar import *
import unittest

class AttackTests(unittest.TestCase):
    def test_basic_melee_attack(self):
        p = Player()
        p.current_action_points = 20
        p.name = 'Player'
        dungeon = Dungeon()
        r = Room(dungeon)
        p.on_move(r)
        self.assertIn(p, r.contents)

        w = Sword()
        p.inventory.append(w)
        p.right = w

        e = Lifeform()
        e.name = 'test'
        e.on_move(r)

        a = Attack()
        a.world = dungeon
        a.player_info = p
        a.args = {'weapon': w.uuid, 'interaction_target': e.uuid}
        result = a.execute()

        self.assertEqual(p.health, 4)
        self.assertTrue(result.success)

    def test_basic_ranged_attack_no_ammo(self):
        p = Player()
        p.current_action_points = 20
        p.name = 'Player'
        dungeon = Dungeon()
        r = Room(dungeon)
        p.on_move(r)
        self.assertIn(p, r.contents)

        w = Bow()
        p.inventory.append(w)
        p.right = w

        e = Lifeform()
        e.name = 'test'
        e.on_move(r)

        a = Attack()
        a.world = dungeon
        a.player_info = p
        a.args = {'weapon': w.uuid, 'interaction_target': e.uuid}
        result = a.execute()

        self.assertEqual(p.health, 4)
        self.assertFalse(result.success)

    def test_basic_ranged_attack_with_ammo(self):
        p = Player()
        p.current_action_points = 20
        p.name = 'Player'
        dungeon = Dungeon()
        r = Room(dungeon)
        p.on_move(r)
        self.assertIn(p, r.contents)

        w = Bow()
        p.inventory.append(w)
        p.right = w

        ar = Arrow()
        ar.on_take(p)
        p.inventory.append(ar)
        p.ammunition = ar

        e = Lifeform()
        e.name = 'test'
        e.on_move(r)

        a = Attack()
        a.world = dungeon
        a.player_info = p
        a.args = {'weapon': w.uuid, 'interaction_target': e.uuid}
        result = a.execute()

        self.assertEqual(p.health, 4)
        self.assertTrue(result.success)

    def test_basic_melee_attack_no_weapon(self):
        p = Player()
        p.current_action_points = 20
        p.name = 'Player'
        dungeon = Dungeon()
        r = Room(dungeon)
        p.on_move(r)
        self.assertIn(p, r.contents)

        e = Lifeform()
        e.name = 'test'
        e.on_move(r)

        a = Attack()
        a.world = dungeon
        a.player_info = p
        a.args = {'interaction_target': e.uuid}
        result = a.execute()

        self.assertEqual(p.health, 4)
        self.assertFalse(result.success)

    def test_basic_melee_attack_no_ap(self):
        p = Player()
        p.name = 'Player'
        dungeon = Dungeon()
        r = Room(dungeon)
        p.on_move(r)
        self.assertIn(p, r.contents)

        w = Sword()
        p.inventory.append(w)
        p.right = w

        e = Lifeform()
        e.name = 'test'
        e.on_move(r)

        a = Attack()
        a.world = dungeon
        a.player_info = p
        a.args = {'weapon': w.uuid, 'interaction_target': e.uuid}
        result = a.execute()

        self.assertEqual(p.health, 4)
        self.assertFalse(result.success)
