from pynarpg.lifeforms.Player import Player
from pynarpg.model.Command import Command
from pynarpg.model.PlayerNode import PlayerNode
from pynarpg.environment.Room import Room
from pynarpg.node.DataAccess import DataAccess
from pynarpg.inventory.Weapon import Weapon
import unittest

class CommandTests(unittest.TestCase):
    def test_find_player(self):
        c = Command()
        c.sender_uid = 'auid'

        d = DataAccess()
        d.players.append(PlayerNode('auid', None))
        c.data = d

        result = c.find_player()

        self.assertEqual(result.uid, 'auid')

    def test_find_in_room(self):
        c = Command()
        w = Weapon()
        r = Room()
        r.contents.append(w)

        result = c.find_in_room(r, w.item_type)

        self.assertEqual(w, result)

    def test_find_in_inventory(self):
        c = Command()
        p = Player()
        w = Weapon()

        p.uid = 'Bob'
        p.inventory.append(w)
        n = PlayerNode(p.uid, p)

        result = c.find_in_inventory(n, w.item_type)

        self.assertEqual(w, result)