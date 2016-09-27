from erukar import *
import unittest

class MoveTests(unittest.TestCase):
    def test_execute_through_wall(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        r = Room(Dungeon())
        p.current_room = r

        m = Move()
        m.sender_uid = p.uid
        m.data = data_store

        m.user_specified_payload = 'north'
        result = m.execute()

        self.assertEqual(result.result_for('Bob')[0], Move.move_through_wall)

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

        m = Move()
        m.sender_uid = p.uid
        m.data = data_store

        m.user_specified_payload = 'south'
        result = m.execute()

        self.assertEqual(result.result_for('Bob')[0], Move.move_through_closed_door)

    def test_execute_through_open_door(self):
        p = Player()
        p.uid = 'Bob'

        data_store = DataAccess()
        data_store.players.append(PlayerNode(p.uid, p))

        d = Dungeon()
        n = Room(d)
        p.current_room = n
        s = Room(d)
        d = Door()
        d.status = Door.Open
        n.coestablish_connection(Direction.South, s, d)

        m = Move()
        m.sender_uid = p.uid
        m.data = data_store

        m.user_specified_payload = 'south'
        result = m.execute()

        self.assertTrue('You have successfully moved South.' in result.result_for('Bob')[0])
        self.assertEqual(p.current_room, s)
