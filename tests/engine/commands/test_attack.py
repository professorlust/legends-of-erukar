from erukar import *
import unittest

class AttackTests(unittest.TestCase):
    def test_basic_attack(self):
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
        self.assertTrue(result.success)
