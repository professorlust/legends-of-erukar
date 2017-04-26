from erukar import *
import unittest

class BasicInteractionTests(unittest.TestCase):
    def test_execute_close_through_wall(self):
        p = Player()
        dungeon = Dungeon()

        r = Room(dungeon)
        p.current_room = r

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': None}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], BasicInteraction.nesw_no_door)
        o.world = dungeon

    def test_execute_close_on_locked_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.current_room = n
        d.lock = Lock()
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.already_closed)

    def test_execute_close_through_closed_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        p.current_room = n
        d = Door()
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.already_closed)


    def test_execute_close_through_open_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.current_room = n
        d.status = Door.Open
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.close_success)
        self.assertEqual(d.status, Door.Closed)

    def test_execute_close_on_chest(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        p.current_room = n
        chest = Container(aliases=['chest'])
        n.add(item=chest)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': chest.uuid}
        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], 'Closed a chest')

    def test_execute_open_through_wall(self):
        p = Player()
        dungeon = Dungeon()

        r = Room(dungeon)
        p.current_room = r

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': None}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], BasicInteraction.nesw_no_door)
        o.world = dungeon

    def test_execute_open_on_locked_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.current_room = n
        d.lock = Lock()
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.already_opened)

    def test_execute_open_through_opened_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        p.current_room = n
        d = Door()
        d.status = Door.Open
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.already_opened)


    def test_execute_open_through_closed_door(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.current_room = n
        d.status = Door.Closed
        n.coestablish_connection(Direction.South, s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], Door.open_success)
        self.assertEqual(d.status, Door.Open)

    def test_execute_open_on_chest(self):
        p = Player()
        dungeon = Dungeon()

        n = Room(dungeon)
        p.current_room = n
        chest = Container(aliases=['chest'])
        n.add(item=chest)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': chest.uuid}
        result = o.execute()

        self.assertEqual(result.result_for(p.uuid)[0], 'Opened a chest')
