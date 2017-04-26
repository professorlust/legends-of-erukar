from erukar import *
import unittest

class TakeTests(unittest.TestCase):
    def test_take_execution(self):
        p = Player()
        dungeon = Dungeon()

        w = Weapon()
        r = Room(dungeon)
        r.add(w)
        r.add(p)
        p.link_to_room(r)

        p.index_item(w, r)

        # Now take it
        t = Take()
        t.world = dungeon
        t.player_info = p
        t.args = {'interaction_target': w.uuid}
        result = t.execute()

        self.assertTrue(w in p.inventory)
        self.assertTrue(w not in r.contents)
        self.assertTrue(result.success)

    def test_take_execution_no_match(self):
        p = Player()
        dungeon = Dungeon()

        w = Weapon()
        r = Room(dungeon)
        r.add(w); r.add(p)
        p.current_room = r

        t = Take()
        t.world = dungeon
        t.player_info = p
        t.args = {'interaction_target': w.uuid}
        result = t.execute()

        self.assertTrue(w in r.contents)
        self.assertTrue(w not in p.inventory)
        self.assertFalse(result.success)
