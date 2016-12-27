from erukar import *
import unittest

class PlayerTests(unittest.TestCase):
    def test_calculate_armor_class_no_armor(self):
        p = Player()
        p.dexterity = 2
        ac = p.evasion()

        self.assertEqual(12, ac)

    def test_skill_roll_string_positive_mod(self):
        p = Player()
        p.dexterity = 2
        dex_srs = p.stat_random_range('dexterity')
        self.assertEqual((2,52), dex_srs)

    def test_skill_roll_string_negative_mod(self):
        p = Player()
        dex_srs = p.stat_random_range('dexterity')
        self.assertEqual((0,50), dex_srs)
