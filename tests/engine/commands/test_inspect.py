from erukar import *
import unittest

class InspectTests(unittest.TestCase):
    def test_inspect_no_target(self):
        p = Player()
        dungeon = Dungeon()

        w = Weapon()
        r = Room(dungeon)
        r.add(w)
        r.add(p)
        p.room = r

        # Now take it
        i = Inspect()
        i.world = dungeon
        i.player_info = p
        i.args = {'a': w.uuid}
        result = i.execute()

        self.assertTrue(result.success)

    def test_inspect_not_enough_ap(self):
        p = Player()
        p.action_points = 1
        dungeon = Dungeon()

        w = Weapon()
        r = Room(dungeon)
        r.add(w)
        r.add(p)
        p.on_move(r)

        # Now take it
        i = Inspect()
        i.world = dungeon
        i.player_info = p
        i.args = {'interaction_target': w.uuid}
        result = i.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Inspect.NotEnoughAP)
        self.assertFalse(result.success)

    def test_inspect_success(self):
        p = Player()
        p.action_points = 2
        dungeon = Dungeon()

        w = Weapon()
        r = Room(dungeon)
        r.add(w)
        r.add(p)
        p.on_move(r)

        # Now take it
        i = Inspect()
        i.world = dungeon
        i.player_info = p
        i.args = {'interaction_target': w.uuid}
        result = i.execute()

        self.assertTrue(result.success)
