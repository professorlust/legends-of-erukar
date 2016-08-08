from erukar import *
import unittest

class TakeTests(unittest.TestCase):
    def test_take_execution(self):
        p = Player()
        p.uid = 'Bob'

        pn = PlayerNode(p.uid, p)
        data_store = DataAccess()
        data_store.players.append(pn)

        w = Weapon()
        w.name = 'Sword'
        r = Room(None)
        r.add(w)
        p.link_to_room(r)
        pn.move_to_room(r)

        # Inspect the room to index the item
        i = Inspect()
        i.sender_uid = p.uid
        i.data = data_store
        i.execute()

        # Now take it
        t = Take()
        t.sender_uid = p.uid
        t.data = data_store
        t.payload = 'sword'
        result = t.execute()

        self.assertTrue(w in p.inventory)
        self.assertTrue(w not in r.contents)
        self.assertEqual(result, Take.success.format('Sword'))

    def test_take_execution_no_match(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        w = Weapon()
        w.name = 'Firearm'
        r = Room(None)
        p.current_room = r
        r.contents.append(w)

        t = Take()
        t.sender_uid = p.uid
        t.data = data_store
        t.payload = 'Sword'
        result = t.execute()

        self.assertTrue(w in r.contents)
        self.assertTrue(w not in p.inventory)
        self.assertEqual(result, Take.failure.format('Sword'))
