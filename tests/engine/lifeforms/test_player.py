from erukar import *
import unittest

class PlayerTests(unittest.TestCase):
    def test_calculate_armor_class_no_armor(self):
        p = Player()
        p.define_stats({ Lifeform.armor_attribute: 2 })
        ac = p.calculate_armor_class()

        self.assertEqual(12, ac)

    def test_calculate_armor_class_with_armor(self):
        p = Player()
        p.define_stats({ Lifeform.armor_attribute: 2 })

        test_armor = Armor()
        test_armor.armor_class_mod = 2
        test_armor.max_dex_mod = 2
        p.chest = test_armor

        ac = p.calculate_armor_class()
        self.assertEqual(14, ac)

    def test_skill_roll_string_positive_mod(self):
        p = Player()
        p.define_stats( { Lifeform.attack_roll_attribute: 2 } )
        dex_srs = p.skill_range(Lifeform.attack_roll_attribute)
        self.assertEqual((3,24), dex_srs)

    def test_skill_roll_string_negative_mod(self):
        p = Player()
        dex_srs = p.skill_range(Lifeform.attack_roll_attribute)
        self.assertEqual((1,20), dex_srs)

