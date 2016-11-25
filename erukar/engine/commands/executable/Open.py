from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Door import Door
import erukar

class Open(ActionCommand):
    nesw_no_door = 'There is no door in this direction to open'
    nesw_wall = 'You cannot open a wall'
    not_found = 'There is nothing to open'

    aliases = ['open']
    TrackedParameters = ['target']

    # I'm not terribly happy with this, as it forces usage of only Doors.
    def execute(self):
        failure = self.check_for_arguments()
        if failure: return failure

        # If the payload was NESW, treat this as a door
        if isinstance(self.target, erukar.engine.model.Direction):
            return self.handle_door()

        # Otherwise we need to find in the room
        self.append_result(self.sender_uid, self.target.on_open(self.player))
        return self.succeed()

    def handle_door(self):
        '''
        Treat this command as an open doors command, since the user typed in
        a direction
        '''
        in_direction = self.room.get_in_direction(self.target)

        # No connections have been made in this direction
        if in_direction is None:
            return self.fail(Open.nesw_wall)

        # determine if the door prevents movement
        door = in_direction.door
        if door is None:
            # There is no door to open
            return self.fail(Open.nesw_no_door)

        self.append_result(self.sender_uid, door.on_open(self.player))
        return self.succeed()
