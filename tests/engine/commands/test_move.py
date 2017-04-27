from erukar import *
import unittest

class MoveTests(unittest.TestCase):
    def test_execute_through_wall(self):
        p = Player()
        d = Dungeon()
        r = Room(d)
        r.add(p)

        m = Move()
        m.player_info = p
        m.args = {'a': 'b'}
        m.world = d
        result = m.execute()

        self.assertFalse(result.success)

    def test_execute_basic(self):
        d = Dungeon()
        e = Room(d)
        w = Room(d)
        e.connect(w)

        p = Player()
        e.add(p)
        p.room = e

        m = Move()
        m.player_info = p
        m.args = {'passage': e.connections[0].uuid}
        m.world = d
        result = m.execute()

        self.assertTrue(p in w.contents)
        self.assertFalse(p in e.contents)
        self.assertTrue(result.success)

