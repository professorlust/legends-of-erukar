from erukar import *
import unittest, random

class RpgEntityTests(unittest.TestCase):
    def test_mitigation_at_zero_should_be_full(self):
        rpgent = RpgEntity()
        rpgent.BaseDamageMitigations['any'] = (0.0, 0)

        mit = rpgent.mitigation('any')

        self.assertEqual(mit, 1.0)

    def test_mitigation_at_full_should_be_zero(self):
        rpgent = RpgEntity()
        rpgent.BaseDamageMitigations['any'] = (1.0, 0)

        mit = rpgent.mitigation('any')

        self.assertEqual(mit, 0.0)

    def test_mitigation_at_negative_should_be_higher(self):
        rpgent = RpgEntity()
        rpgent.BaseDamageMitigations['any'] = (-1.0, 0)

        mit = rpgent.mitigation('any')

        self.assertEqual(mit, 2.0)

    def test_negative_mitigation_should_yield_higher_damage_taken(self):
        rpgent = RpgEntity()
        rpgent.BaseDamageMitigations['any'] = (-1.0, 0)

        actual = sum(x[0] for x in Damage.actual_damage_values(rpgent, rpgent, None, [(1, 'any')]))
        self.assertEqual(actual, 2.0)
