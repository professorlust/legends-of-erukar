import unittest
import erukar
from erukar import ActivateAbility, Enemy, Attack
from erukar.ext.math import Shapes
from erukar.content.modifiers.gameplay.enhancement import HealthEnhancement


class HealthEnhancement_Test(unittest.TestCase):
    def setUp(self):
        dungeon = erukar.FrameworkDungeon()
        erukar.Room(dungeon, coordinates=Shapes.rect((-2, -2), (2, 2)))
        self.interface = erukar.TestInterface(dungeon=dungeon)
        self.interface.dungeon.actors = set()
        self.player = self.interface.player
        self.player.uid = 'test'
        self.basic_data = {
            'player_lifeform': self.player
        }
        dungeon.add_actor(self.player, (0, 0))
        self.player.gain_action_points()

    def test__integration__health_enhancement(self):
        item = erukar.Longsword(modifiers=[HealthEnhancement])
        health = self.player.maximum_health()
        self.player.left = item
        self.player.inventory = [item]
        item.on_equip(self.player)
        self.assertGreater(self.player.maximum_health(), health)
