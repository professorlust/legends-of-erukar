from erukar import *
import unittest

class CloseTests(unittest.TestCase):
    def test_execute_through_wall(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        r = Room(None)
        p.current_room = r

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store
        o.user_specified_payload = 'north'

        result = o.execute()

        self.assertEqual(result.result, Close.nesw_no_door)

    def test_execute_through_no_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        s = Room(None)
        n.coestablish_connection(Direction.South, s, None)

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store
        o.user_specified_payload = 'south'

        result = o.execute()

        self.assertEqual(result.result, Close.nesw_no_door)

    def test_execute_through_locked_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        s = Room(None)
        d = Door()
        p.current_room = n
        d.lock = Lock()
        n.coestablish_connection(Direction.South, s, d)

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store
        o.user_specified_payload = 'south'

        result = o.execute()

        self.assertEqual(result.result, Door.already_closed)

    def test_execute_through_closed_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        s = Room(None)
        p.current_room = n
        d = Door()
        n.coestablish_connection(Direction.South, s, d)

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store
        o.user_specified_payload = 'south'

        result = o.execute()

        self.assertEqual(result.result, Door.already_closed)


    def test_execute_through_open_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        s = Room(None)
        d = Door()
        p.current_room = n
        d.status = Door.Open
        n.coestablish_connection(Direction.South, s, d)

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store

        o.user_specified_payload = 'south'

        result = o.execute()

        self.assertEqual(result.result, Door.close_success)
        self.assertEqual(d.status, Door.Closed)

    def test_execute_on_chest(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        n = Room(None)
        p.current_room = n
        chest = Container(aliases=['chest'])
        n.add(item=chest)

        o = Close()
        o.sender_uid = p.uid
        o.data = data_store

        o.user_specified_payload = 'chest'

        result = o.execute()

        self.assertEqual(result.result, 'Closed a chest')
