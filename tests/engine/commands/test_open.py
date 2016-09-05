from erukar import *
import unittest

class OpenTests(unittest.TestCase):
    def test_execute_through_wall(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        r = Room(None)
        p.current_room = r

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'north'
        result = o.execute()

        self.assertEqual(result, Open.nesw_no_door)

    def test_execute_through_no_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        s = Room(None)
        n.coestablish_connection(Direction.South, s, None)

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'south'
        result = o.execute()

        self.assertEqual(result, Open.nesw_no_door)

    def test_execute_through_locked_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        s = Room(None)
        d = Door()
        d.lock = Lock()
        n.coestablish_connection(Direction.South, s, d)

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'south'
        result = o.execute()

        self.assertEqual(result, Door.is_locked)

    def test_execute_through_open_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        s = Room(None)
        d = Door()
        d.status = Door.Open
        n.coestablish_connection(Direction.South, s, d)

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'south'
        result = o.execute()

        self.assertEqual(result, Door.already_open)

    def test_execute_through_closed_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        s = Room(None)
        d = Door()
        n.coestablish_connection(Direction.South, s, d)

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'south'
        result = o.execute()

        self.assertEqual(result, Door.open_success)
        self.assertEqual(d.status, Door.Open)

    def test_execute_on_chest(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        chest = Container(aliases=['chest'])
        n.add(chest)

        o = Open()
        o.sender_uid = p.uid
        o.data = data_store

        o.payload = 'chest'
        result = o.execute()

        self.assertEqual(result, 'Opened a chest')
