from erukar import *
import unittest

class LifeformTests(unittest.TestCase):
    def test_define_stats_no_entry(self):
        # Test Case: 0 0 0
        l = Lifeform()

        self.assertEqual(l.strength, 0)
        self.assertEqual(l.dexterity, 0)
        self.assertEqual(l.vitality, 0)

    def test_define_stats_stronly(self):
        # Test Case: 2 0 0
        l = Lifeform()
        l.strength = 2
        self.assertEqual(l.strength, 2)
        self.assertEqual(l.dexterity, 0)
        self.assertEqual(l.vitality, 0)

    def test_define_stats_dexonly(self):
        # Test Case: 0 2 0
        l = Lifeform()
        l.dexterity = 2
        self.assertEqual(l.strength, 0)
        self.assertEqual(l.dexterity, 2)
        self.assertEqual(l.vitality, 0)

    def test_define_stats_vitonly(self):
        # Test Case: 0 0 2
        l = Lifeform()
        l.vitality = 2
        self.assertEqual(l.strength, 0)
        self.assertEqual(l.dexterity, 0)
        self.assertEqual(l.vitality, 2)

    def test_define_level_creates_appropriate_health(self):
        l = Lifeform()
        l.define_level(3)
        self.assertEqual(4*3, l.health)

    def test_take_damage_not_fatal(self):
        l = Lifeform()
        l.vitality = 2
        l.define_level(3)

        l.take_damage(4)
        self.assertTrue('dying' not in l.conditions)

    def test_take_damage_fatal(self):
        l = Lifeform()
        l.define_level(1)

        l.take_damage(5)
        self.assertTrue(l.has_condition(Dying))

    def test_take_damage_coup_de_grace(self):
        l = Lifeform()
        l.define_level(1)

        Dead(l)

        l.take_damage(5)
        self.assertTrue(l.has_condition(Dead))

    def consume_action_point_should_take_from_current_first(self):
        l = Lifeform()
        cost = 1
        self.assertTrue(False)
#       l.current_action_points = 2
#       l.reserved_action_points = 2

#       l.consume_action_point(cost)
#       self.assertEqual(l.current_action_points, 0)
#       self.assertEqual(l.reserved_action_points, 2)
