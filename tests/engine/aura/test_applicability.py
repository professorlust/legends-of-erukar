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
