from erukar import *
from erukar.game.modifiers.inventory.Broken import Broken
import unittest

class WeaponModTests(unittest.TestCase):
    def test_apply_to_weapon_actually_applies(self):
        w = Weapon()
        mod = Broken()
        mod.modify(w)

        self.assertTrue('Broken' in w.name)

    def test_apply_to_item_does_not_apply(self):
        i = Item()
        mod = WeaponMod()
        mod.modify(i)

        self.assertFalse(hasattr(i, 'damage'))
