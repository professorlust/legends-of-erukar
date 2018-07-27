from .Instance import Instance

class HubInstance(Instance):
    def try_execute(self, node, cmd):
        cmd.interactions = self.active_interactions
        if not self.any_connected_players():
            if isinstance(self.active_player, Enemy):
                self.active_player.stop_execution()
            return

        if isinstance(cmd, TargetedCommand):
            return self.try_execute_targeted_command(node, cmd)

        self.execute_and_process(cmd)

        # Tell characters
        self.send_update_to_players()
        self.handle_all_transitions()
