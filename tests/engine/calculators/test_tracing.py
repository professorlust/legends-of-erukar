from erukar import *
import erukar, math
import unittest

class TracingTests(unittest.TestCase):
    def test_raytrace_yields_finish_if_no_obstruction(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, None)

        result = Navigator.raytrace(l, r)
        self.assertEqual(result, r)

    def test_raytrace_yields_collision_if_obstructed(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, Door())

        result = Navigator.raytrace(l, r)
        self.assertEqual(result, m)

    def test_raytrace_yields_collision_if_obstructedi_but_door_is_open(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        door = Door()
        door.status = Door.Open
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, door)

        result = Navigator.raytrace(l, r)
        self.assertEqual(result, r)

    def test_angle_results_are_coherent(self):
        payloads = [
            ((0,0), (1,0), 0),
            ((0,0), (0,1), math.pi/2),
            ((0,0), (-1,0), math.pi),
            ((0,0), (0,-1), 3*math.pi/2),
        ]

        for start, finish, result in payloads:
            angle = Navigator.angle(start, finish)
            self.assertEqual(angle, result)

    def test_light_obstruction(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, Door())
        
        a = Aura((2,0))
        a.blocked_by_walls = True
        a.aura_strength = 1000
        r.initiate_aura(a)

        self.assertEqual(len(list(d.get_applicable_auras(l))), 0)
