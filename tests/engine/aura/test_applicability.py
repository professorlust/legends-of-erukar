from erukar import *
import unittest

class ApplicabilityTests(unittest.TestCase):
    def test_does_affect_within_range(self):
        aura = Aura((0, 0))

        d = Dungeon()
        center = Room(d,(0,0))
        center.initiate_aura(aura)
        e = Room(d, (1,0))
        n = Room(d, (0,1))
        w = Room(d, (-1,0))
        s = Room(d, (0,-1))
        center.connect(e, None)
        center.connect(n, None)
        center.connect(w, None)
        center.connect(s, None)

        self.assertTrue(aura.affects_tile(center))
        self.assertTrue(aura.affects_tile(e))
        self.assertTrue(aura.affects_tile(n))
        self.assertTrue(aura.affects_tile(w))
        self.assertTrue(aura.affects_tile(s))

    def test_does_not_affect_outside_range(self):
        aura = Aura((0, 0))
        d = Dungeon()
        center = Room(d,(0,0))
        center.initiate_aura(aura)
        e = Room(d, (1,0))
        n = Room(d, (0,1))
        w = Room(d, (-1,0))
        s = Room(d, (0,-1))
        ee = Room(d, (2,0))
        nn = Room(d, (0,2))
        ww = Room(d, (-2,0))
        ss = Room(d, (0,-2))
        center.connect(e, None)
        e.connect(ee, None)
        center.connect(n, None)
        n.connect(nn, None)
        center.connect(w, None)
        w.connect(ww, None)
        center.connect(s, None)
        s.connect(ss, None)

        self.assertFalse(aura.affects_tile(ee))
        self.assertFalse(aura.affects_tile(nn))
        self.assertFalse(aura.affects_tile(ww))
        self.assertFalse(aura.affects_tile(ss))

    def test_dungeon_gets_only_applicable(self):
        d = Dungeon()

        l = Room(d, (0,0))
        m = Room(d, (1,0))
        r = Room(d, (2,0))
        a1 = Aura(l)
        a2 = Aura(m)
        a3 = Aura(r)

        l.connect(m, None)
        m.connect(r, None)
        d.active_auras = set([a1, a2, a3])
        d.rooms = [l,m,r]

        applicable = list(d.get_applicable_auras(l))

        self.assertIn(a1, applicable)
        self.assertIn(a2, applicable)
        self.assertNotIn(a3, applicable)


    def test_dungeon_auras_for_locations_gets_all(self):
        d = Dungeon()
        l = Room(d, (0,0))
        c = Room(d, (1,0))
        l.connect(c, None)
        r = Room(d, (2,0))
        c.connect(r, None)

        locations = [l,c]
        a1 = Aura(l)
        a2 = Aura(c)
        a3 = Aura(r)
        a3.decay_factor = 0.5
        a3.strength = 2

        d.rooms = [l,c,r]
        d.active_auras = set([a1, a2, a3])
        results = d.auras_for_locations(locations)

        self.assertIn(a1, results[l])
        self.assertIn(a1, results[c])

        self.assertIn(a2, results[l])
        self.assertIn(a2, results[c])

        self.assertNotIn(a3, results[l])
        self.assertIn(a3, results[c])

    def test_dungeon_cleanup(self):
        d = Dungeon()
        l = Room(d, [(0,0)])
        r = Room(d, [(1,0)]) 
        d.rooms = [l, r]

        a1 = Aura(l)
        a2 = Aura(l)
        a3 = Aura(r)
        d.active_auras = set([a1, a2, a3])
        first_results = list(d.get_applicable_auras(l))

        self.assertIn(a1, first_results) 
        self.assertIn(a2, first_results) 
        self.assertIn(a3, first_results) 

        a1.is_expired = True
        d.clean_up_auras()

        second_results = list(d.get_applicable_auras(l))

        self.assertNotIn(a1, second_results) 
        self.assertIn(a2, second_results) 
        self.assertIn(a3, second_results) 

    def test_auras_can_move(self):
        d = Dungeon()
        l = Room(d, (0,0))
        r = Room(d, (1,0)) 
        d.rooms = [l, r]
        l.connect(r,None)

        a1 = Aura(l)
        a1.strength = 1
        a1.decay_factor = 0
        d.active_auras = set([a1])

        first = list(d.get_applicable_auras(r))
        self.assertNotIn(a1, first)

        a1.location = r
        second = list(d.get_applicable_auras(r))
        self.assertIn(a1, second)

    def test_lighting(self):
        def modify_light(decay):
            return 0.5

        d = Dungeon()
        l = Room(d, (0,0))
        r = Room(d, (1,0))
        l.connect(r, None)
        d.rooms = [l, r]

        a1 = Aura(l)
        a1.decay_factor = 0
        d.active_auras = set([a1])
        a1.modify_light = modify_light
        self.assertTrue(hasattr(a1, 'modify_light'))

        first = r.calculate_luminosity()
        self.assertEqual(first, 0.0)

        a1.location = r
        second = r.calculate_luminosity()
        self.assertEqual(second, 0.5)
