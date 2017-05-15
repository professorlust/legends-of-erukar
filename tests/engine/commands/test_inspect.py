from erukar import *
import unittest

class InspectTests(unittest.TestCase):
    def test_inspect_no_target(self):
        p = Player()
        p.current_action_points = 20
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
        i.args = {'a': str(w.uuid)}
        result = i.execute()

        self.assertTrue(result.success)

    def test_inspect_not_enough_ap(self):
        p = Player()
        p.uid = 'Evan'
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
        i.args = {'interaction_target': str(w.uuid)}
        result = i.execute()

        self.assertFalse(result.success)
        self.assertEqual(result.result_for(p.uid)[0], Inspect.NotEnoughAP)

    def test_inspect_success(self):
        p = Player()
        p.current_action_points = 20
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
        i.args = {'interaction_target': str(w.uuid)}
        result = i.execute()

        self.assertTrue(result.success)
