from erukar import *
import unittest

class BasicInteractionTests(unittest.TestCase):
    def test_execute_close_through_wall(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        r = Room(dungeon)
        p.room = r

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': None}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], BasicInteraction.NoTarget)

    def test_execute_close_on_locked_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.room = n
        d.lock = Lock()
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.already_closed)

    def test_execute_close_through_closed_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        p.room = n
        d = Door()
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.already_closed)


    def test_execute_close_through_open_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.room = n
        d.status = Door.Open
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.close_success)
        self.assertEqual(d.status, Door.Closed)

    def test_execute_close_on_chest(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        p.room = n
        chest = Container(aliases=['chest'])
        n.add(item=chest)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'close', 'interaction_target': chest.uuid}
        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], 'Closed a chest')

    def test_execute_open_through_wall(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        r = Room(dungeon)
        p.room = r

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': None}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], BasicInteraction.NoTarget)
        o.world = dungeon

    def test_execute_open_on_locked_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.room = n
        d.lock = Lock()
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.is_locked)

    def test_execute_open_through_opened_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        p.room = n
        d = Door()
        d.status = Door.Open
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.already_open)

    def test_execute_open_through_closed_door(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        s = Room(dungeon)
        d = Door()
        p.room = n
        d.status = Door.Closed
        n.connect(s, d)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': d.uuid}

        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Door.open_success)
        self.assertEqual(d.status, Door.Open)

    def test_execute_open_on_chest(self):
        p = Player()
        p.current_action_points = 20
        dungeon = Dungeon()

        n = Room(dungeon)
        p.room = n
        chest = Container(aliases=['chest'])
        n.add(item=chest)

        o = BasicInteraction()
        o.world = dungeon
        o.player_info = p
        o.args = {'interaction_type': 'open', 'interaction_target': chest.uuid}
        result = o.execute()

        self.assertEqual(result.result_for(p.uid)[0], Container.Opened)
