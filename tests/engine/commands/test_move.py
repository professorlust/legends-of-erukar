from erukar import *
import unittest

class MoveTests(unittest.TestCase):
    def test_execute_through_wall(self):
        d = Dungeon()
        p = Player(d)
        r = Room(d, [(0,1)])
        r.add(p)

        m = Move()
        m.player_info = p
        m.args = {'a': 'b'}
        m.world = d
        result = m.execute()

        self.assertFalse(result.success)
