from erukar import *
import unittest

class CommandTests(unittest.TestCase):
    def test_find_player(self):
        c = Command()
        c.sender_uid = 'auid'

        d = DataAccess()
        d.players.append(PlayerNode('auid', None))
        c.data = d

        result = c.find_player()

        self.assertEqual(result.uid, 'auid')

    def test_determine_direction_n(self):
        m = Command()
        result = m.determine_direction('n')

        self.assertEqual(result, Direction.North)

    def test_determine_direction_north(self):
        m = Command()
        result = m.determine_direction('north')

        self.assertEqual(result, Direction.North)

    def test_determine_direction_e(self):
        m = Command()
        result = m.determine_direction('e')

        self.assertEqual(result, Direction.East)

    def test_determine_direction_east(self):
        m = Command()
        result = m.determine_direction('east')

        self.assertEqual(result, Direction.East)

    def test_determine_direction_s(self):
        m = Command()
        result = m.determine_direction('s')

        self.assertEqual(result, Direction.South)

    def test_determine_direction_south(self):
        m = Command()
        result = m.determine_direction('south')

        self.assertEqual(result, Direction.South)

    def test_determine_direction_w(self):
        m = Command()
        result = m.determine_direction('w')

        self.assertEqual(result, Direction.West)

    def test_determine_direction_west(self):
        m = Command()
        result = m.determine_direction('west')

        self.assertEqual(result, Direction.West)
