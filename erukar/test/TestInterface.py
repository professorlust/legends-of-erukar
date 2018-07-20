from erukar import Lifeform
from .TestInstance import TestInstance
from .TestDungeonGenerator import TestDungeonGenerator


class TestInterface:
    def __init__(self, player=None, instance=None, dungeon=None):
        self.player = player or Lifeform()
        self.dungeon = TestDungeonGenerator().generate()
        self.instance = instance or TestInstance(self.dungeon)
        self.instance.subscribe_being(self.player)

    def create_command(self, cmd_type, data):
        cmd = cmd_type()
        cmd.world = self.dungeon
        cmd.args = data
        cmd.player_info = self.player
        return cmd

    def exec_command(self, cmd_type, data):
        cmd = self.create_command(cmd_type, data)
        return self.instance.try_execute(self.player, cmd)

    def exec_and_log(self, cmd_type, data):
        res = self.exec_command(cmd_type, data)
        return res.results[self.player.uid]
