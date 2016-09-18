from erukar import *
import unittest

class ApplicabilityTests(unittest.TestCase):
    def test_does_affect_within_range(self):
        aura = Aura((0, 0))

        self.assertTrue(aura.affects_tile((0,0)))
        self.assertTrue(aura.affects_tile((0,-1)))
        self.assertTrue(aura.affects_tile((-1,0)))
        self.assertTrue(aura.affects_tile((1,0)))
        self.assertTrue(aura.affects_tile((0,1)))

    def test_does_not_affect_outside_range(self):
        aura = Aura((0, 0))

        self.assertFalse(aura.affects_tile((1,-1)))
        self.assertFalse(aura.affects_tile((1,1)))
        self.assertFalse(aura.affects_tile((-1,-1)))
        self.assertFalse(aura.affects_tile((-1,1)))
        self.assertFalse(aura.affects_tile((0,-2)))
        self.assertFalse(aura.affects_tile((-2,0)))
        self.assertFalse(aura.affects_tile((2,0)))
        self.assertFalse(aura.affects_tile((0,2)))

    def test_dungeon_gets_only_applicable(self):
        location = (0,0)
        a1 = Aura((0,0))
        a2 = Aura((1,0))
        a3 = Aura((10,0))

        d = Dungeon()
        d.active_auras = set([a1, a2, a3])

        applicable = list(d.get_applicable_auras(location))

        self.assertIn(a1, applicable)
        self.assertIn(a2, applicable)
        self.assertNotIn(a3, applicable)


    def test_dungeon_auras_for_locations_gets_all(self):
        locations = [(0,0), (0,1)]
        a1 = Aura((-1,0))
        a2 = Aura((0,1))
        a3 = Aura((0,2))

        d = Dungeon()
        d.active_auras = set([a1, a2, a3])
        results = d.auras_for_locations(locations)

        self.assertIn(a1, results[(0,0)])
        self.assertNotIn(a1, results[(0,1)])

        self.assertIn(a2, results[(0,0)])
        self.assertIn(a2, results[(0,1)])

        self.assertNotIn(a3, results[(0,0)])
        self.assertIn(a3, results[(0,1)])

    def test_dungeon_cleanup(self):
        location = (0,0)
        a1 = Aura((1,0))
        a2 = Aura((0,1))
        a3 = Aura((0,0))

        d = Dungeon()
        d.active_auras = set([a1, a2, a3])
        first_results = list(d.get_applicable_auras(location))

        self.assertIn(a1, first_results) 
        self.assertIn(a2, first_results) 
        self.assertIn(a3, first_results) 

        a1.is_expired = True
        d.clean_up_auras()

        second_results = list(d.get_applicable_auras(location))

        self.assertNotIn(a1, second_results) 
        self.assertIn(a2, second_results) 
        self.assertIn(a3, second_results) 

    def test_auras_can_move(self):
        location = (0,0)
        a1 = Aura((0, 3))

        d = Dungeon()
        d.active_auras = set([a1])

        first = list(d.get_applicable_auras(location))
        self.assertNotIn(a1, first)

        a1.location = (0,0)
        second = list(d.get_applicable_auras(location))
        self.assertIn(a1, second)

    def test_lighting(self):
        location = (0,0)
        a1 = Aura((20, 20))
        def modify_light():
            return 0.5

        a1.modify_light = modify_light
        self.assertTrue(hasattr(a1, 'modify_light'))

        d = Dungeon()
        d.active_auras = set([a1])
        r = Room(d, (0,0))

        first = r.calculate_luminosity()
        self.assertEqual(first, 0.0)

        a1.location = (1,0)
        second = r.calculate_luminosity()
        self.assertEqual(second, 0.5)
