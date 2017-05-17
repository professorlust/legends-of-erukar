from erukar import *
import unittest

class TakeTests(unittest.TestCase):
    def test_take_execution(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 2

        w = Weapon()
        r = Room(dungeon, [(0,1)])
        r.add(w)
        r.add(p)
        p.on_move(r)

        p.index_item(w, r)

        # Now take it
        t = Take()
        t.world = dungeon
        t.player_info = p
        t.args = {'interaction_target': str(w.uuid)}
        result = t.execute()

        self.assertTrue(result.success)
        self.assertTrue(w in p.inventory)
        self.assertTrue(w not in r.contents)

    def test_take_execution_no_match(self):
        dungeon = Dungeon()
        p = Player(dungeon)
        p.current_action_points = 2

        w = Weapon()
        r = Room(dungeon, [(0,1)])
        r.add(w); r.add(p)
        p.current_room = r

        t = Take()
        t.world = dungeon
        t.player_info = p
        t.args = {'interaction_target': str(w.uuid)}
        result = t.execute()

        self.assertFalse(result.success)
        self.assertTrue(w in r.contents)
        self.assertTrue(w not in p.inventory)
