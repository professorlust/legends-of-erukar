from erukar import *
import unittest

class InventoryTests(unittest.TestCase):
    def test_describe_with_suffix(self):
        i = Item(name='Bastard Sword')

        result = i.describe()

        self.assertEqual(result, "Bastard Sword")

