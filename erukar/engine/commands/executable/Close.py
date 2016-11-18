from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Door import Door
import erukar

class Close(ActionCommand):
    nesw_no_door = 'There is no door in this direction to close'
    nesw_wall = 'You cannot close a wall'
    not_found = 'There is nothing to close'

    aliases = ['close', 'shut']
    TrackedParameters = ['target']

    def execute(self):
        self.player = self.find_player()
        self.room = self.player.lifeform().current_room
        failure = self.check_for_arguments()
        if failure: return failure

        # If the payload was NESW, treat this as a door
        if isinstance(self.target, erukar.engine.model.Direction):
            return self.handle_door()

        # Otherwise we need to find in the room
        self.append_result(self.sender_uid, self.target.on_close(self.player))
        return self.succeed()

    def handle_door(self):
        '''
        Treat this command as an close doors command, since the user typed in
        a direction
        '''
        in_direction = self.room.get_in_direction(self.target)

        # No connections have been made in this direction
        if in_direction is None:
            return self.fail(Close.nesw_wall)

        # determine if the door prevents movement
        door = in_direction.door
        if door is None:
            # There is no door to close
            return self.fail(Close.nesw_no_door)

        # Have the door handle it now
        result = door.on_close(self.player)
        self.append_result(self.sender_uid, result)
        return self.succeed()
