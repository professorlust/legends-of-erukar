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
