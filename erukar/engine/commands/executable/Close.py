from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Door import Door
import erukar

class Close(ActionCommand):
    def perform(self):
        # If the payload was NESW, treat this as a door
        result = self.args['close_target'].on_close(self.args['player_lifeform'])
        self.append_result(self.sender_uid, close_result)
        return self.succeed()
