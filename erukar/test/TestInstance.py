from erukar import Instance, TargetedCommand


class TestInstance(Instance):
    def __init__(self, dungeon):
        super().__init__(None)
        self.dungeon = dungeon
        self.location = self.dungeon.location

    def send_update_to(self, *_):
        return

    def try_execute(self, node, cmd):
        cmd.interactions = self.active_interactions
        self.active_player = node
        if isinstance(cmd, TargetedCommand):
            return self.try_execute_targeted_command(node, cmd)
        return self.execute_and_process(cmd, False)

    def execute_and_process(self, cmd, auto_advance):
        return self.execute_command(cmd)
