from erukar import *
import unittest

class EquipTests(unittest.TestCase):
    def test_equip_weapon(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        w = Weapon()
        w.name = "Sword"
        p.inventory.append(w)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.user_specified_payload = 'sword'
        result = e.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.right, w)
        self.assertIn('successfully', result.result_for('Bob')[0])

    def test_equip_armor(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        a = Armor('Plate Mail')
        a.equipment_types = ['chest']
        self.assertEqual(a.item_type, 'armor')
        self.assertEqual(a.name, 'Plate Mail')
        p.inventory.append(a)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.user_specified_payload = 'plate mail'
        result = e.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.chest, a)
        self.assertIn('successfully', result.result_for('Bob')[0])

    def test_equip_item(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        i = Item('Potion', 'Potion')
        p.inventory.append(i)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.user_specified_payload = 'potion'
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.chest, i)
        self.assertNotEqual(p.right, i)
        self.assertEqual(Equip.cannot_equip.format('Potion'), result.result_for('Bob')[0])

    def test_equip_no_match(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        i = Item('Potion','Potion')
        p.inventory.append(i)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.user_specified_payload = 'sword'
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.chest, i)
        self.assertNotEqual(p.right, i)
        self.assertEqual(Equip.not_found.format('sword'), result.result_for('Bob')[0])

