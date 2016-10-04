from erukar import *
import unittest

class DungeonGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.gen = DungeonGenerator()
        self.gen.dungeon = Dungeon()

    def test_connect_randomly_should_make_a_connection(self):
        self.gen.dungeon.rooms = [Room(None), Room(None)]
        self.gen.connect_randomly(self.gen.dungeon.rooms[0])

        self.assertTrue(any(self.gen.dungeon.rooms[0].connections[d] for d in self.gen.dungeon.rooms[0].connections))

    def test_connect_rooms_should_make_a_connection(self):
        self.gen.dungeon.rooms = [Room(None), Room(None)]
        self.gen.connect_rooms()

        no_connections = any(self.gen.dungeon.rooms[0].connections[d] for d in self.gen.dungeon.rooms[0].connections)
        self.assertTrue(no_connections)

    def test_fill_walls_should_not_have_abysses(self):
        self.gen.dungeon.rooms = [Room(None)]
        self.gen.fill_walls()
        r = self.gen.dungeon.rooms[0]

        walls = len([self.gen.dungeon.rooms[0].connections[d].door \
            for d in self.gen.dungeon.rooms[0].connections if self.gen.dungeon.rooms[0].connections[d] is not None])
        self.assertEqual(walls, 4)

    def test_possible_directions_should_not_return_a_wall(self):
        self.gen.dungeon.rooms = [Room(None), Room(None)]
        self.gen.connect_rooms()

        dirs = self.gen.possible_directions(self.gen.dungeon.rooms[0])
        self.assertEqual(len(list(dirs)), 3)
