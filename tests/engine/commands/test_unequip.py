from erukar import *
import unittest

class UnequipTests(unittest.TestCase):
    def test_unequip_weapon(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        w = Weapon()
        w.name = 'Sword'
        p.inventory.append(w)
        p.right = w

        u = Unequip()
        u.sender_uid = p.uid
        u.data = data_store
        u.payload = 'sword'
        result = u.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, None)
        self.assertEqual(Unequip.unequipped_right.format(w.name), result)

    def test_unequip_armor(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        a = Armor()
        a.name = 'Plate Mail'
        p.inventory.append(a)
        p.chest = a

        u = Unequip()
        u.sender_uid = p.uid
        u.data = data_store
        u.payload = 'plate mail'
        result = u.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, None)
        self.assertEqual(Unequip.unequipped_chest.format(a.name), result)

    def test_unequip_item(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        i = Item()
        i.item_type = 'Potion'
        p.inventory.append(i)

        u = Unequip()
        u.sender_uid = p.uid
        u.data = data_store
        u.payload = 'potion'
        result = u.execute()

        self.assertTrue(i in p.inventory)
        self.assertEqual(Unequip.not_found.format('potion'), result)
