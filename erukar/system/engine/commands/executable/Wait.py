from ..ActionCommand import ActionCommand

class Wait(ActionCommand):
    RebuildZonesOnSuccess = True
    NeedsArgs = False

    def perform(self):
        self.append_result(self.player_info.uid, 'Waiting')
        return self.succeed()
