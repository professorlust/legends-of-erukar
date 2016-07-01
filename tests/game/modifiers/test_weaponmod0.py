from erukar import *
import unittest

class WeaponModTests(unittest.TestCase):
    def test_apply_to_weapon_actually_applies(self):
        w = Weapon()
        mod = WeaponMod()
        mod.modify(w)

        self.assertEqual(w.damage_range, (0, 1))

    def test_apply_to_item_does_not_apply(self):
        i = Item()
        mod = WeaponMod()
        mod.modify(i)

        self.assertFalse(hasattr(i, 'damage'))
