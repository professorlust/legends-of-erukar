from erukar import *
import unittest

class EquipTests(unittest.TestCase):
    def test_equip_weapon(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        w = Weapon('Sword')
        p.inventory.append(w)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.payload = 'sword'
        result = e.execute()

        self.assertTrue(w in p.inventory)
        self.assertEqual(p.weapon, w)
        self.assertEqual(Equip.equipped_weapon.format('Sword'), result)

    def test_equip_armor(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        a = Armor('Plate Mail')
        self.assertEqual(a.item_type, 'armor')
        self.assertEqual(a.name, 'Plate Mail')
        p.inventory.append(a)

        e = Equip()
        e.sender_uid = p.uid
        e.data = data_store
        e.payload = 'plate mail'
        result = e.execute()

        self.assertTrue(a in p.inventory)
        self.assertEqual(p.armor, a)
        self.assertEqual(Equip.equipped_armor.format('Generic Plate Mail'), result)

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
        e.payload = 'potion'
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.armor, i)
        self.assertNotEqual(p.weapon, i)
        self.assertEqual(Equip.cannot_equip.format('Generic Potion'), result)

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
        e.payload = 'sword'
        result = e.execute()

        self.assertTrue(i in p.inventory)
        self.assertNotEqual(p.armor, i)
        self.assertNotEqual(p.weapon, i)
        self.assertEqual(Equip.not_found.format('sword'), result)


    def test_item_type(self):
        w = Weapon()
        e = Equip()
        result = e.item_type(w)
        self.assertEqual(result, 'weapon')
