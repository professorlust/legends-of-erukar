from erukar import *
import erukar, math
import unittest

class TracingTests(unittest.TestCase):
    def test_aura_directional_descriptions_make_sense(self):
        aura = Aura((0, 0))
        d = Dungeon()
        l = Lifeform()
        center = Room(d,(0,0))
        center.initiate_aura(aura)

        # This iterates over all of the directions and makes sure that the 
        # directions from describe_brief all are coherent (e.g. West -> "... west... ")
        for aux in [((1,0), Direction.West), ((0,-1), Direction.North), ((-1,0), Direction.East), ((0,1), Direction.South)]:
            nr = Room(d, aux[0])
            l.link_to_room(nr)
            center.coestablish_connection(aux[1], nr, None)
            applicable = list(d.get_applicable_auras(nr))
            desc = applicable[0].brief_inspect(l, 50, 50)
            self.assertIn(aux[1].name.lower(), desc)


    def test_raytrace_yields_finish_if_no_obstruction(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, None)

        result = Navigator.raytrace(l, r)
        self.assertEqual(result, r)
        self.assertFalse(Navigator.exists_obstruction_between(r, r))
        self.assertFalse(Navigator.exists_obstruction_between(l, r))

    def test_raytrace_yields_collision_if_obstructed(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, Door())

        result = Navigator.raytrace(l, r)
        self.assertEqual(result, m)
        self.assertTrue(Navigator.exists_obstruction_between(l, r))

    def test_raytrace_yields_collision_if_obstructed_but_door_is_open(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        door = Door()
        door.status = Door.Open
        l.coestablish_connection(Direction.East, m, None)
        m.coestablish_connection(Direction.East, r, door)

        result = Navigator.raytrace(l, r)
        self.assertFalse(Navigator.exists_obstruction_between(l, r))
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
