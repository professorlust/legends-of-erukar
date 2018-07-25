import unittest
import erukar
from erukar import Enemy
from erukar.ext.math import Shapes


class Lifeform_Test(unittest.TestCase):
    def setUp(self):
        dungeon = erukar.FrameworkDungeon()
        erukar.Room(dungeon, coordinates=Shapes.rect((-2, -2), (2, 2)))
        self.interface = erukar.TestInterface(dungeon=dungeon)
        self.interface.dungeon.actors = set()

        self.player = self.interface.player
        self.player.uid = 'test'
        self.player.head = erukar.Helm(modifiers=[erukar.Gold])
        self.player.head.on_start(self.interface.dungeon)

        self.enemy = Enemy()
        self.enemy.left = erukar.Longsword(modifiers=[erukar.Gold])
        self.enemy.left.on_start(self.interface.dungeon)

        dungeon.add_actor(self.player, (0, 0))
        self.player.gain_action_points()

    def test__damage_equipment__does_damage_if_mitigated(self):
        pre_durability = self.player.head.durability
        damage = {
            'slashing': 50
        }
        self.player.apply_damage(self.enemy, self.enemy.left, damage)
        self.assertLess(self.player.head.durability, pre_durability)

    def test__damage_equipment__does_not_damage_if_no_mit(self):
        pre_durability = self.player.head.durability
        damage = {
            'thisIsNotARealDamageType': 50
        }
        self.player.apply_damage(self.enemy, self.enemy.left, damage)
        self.assertEqual(self.player.head.durability, pre_durability)

    def test__damage_weapon(self):
        damage = {
            'slashing': 50
        }
        pre_durability = self.enemy.left.durability
        self.player.apply_damage(self.enemy, self.enemy.left, damage)
        self.assertLess(self.enemy.left.durability, pre_durability)
