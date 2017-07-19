from erukar.engine.commands.ActionCommand import ActionCommand
import erukar

class Wait(ActionCommand):
    RebuildZonesOnSuccess = True
    NeedsArgs = False

    def perform(self):
        self.append_result(self.player_info.uid, 'Waiting')
        return self.succeed()
