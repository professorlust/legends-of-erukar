from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment.Door import Door

class Close(ActionCommand):
    nesw_no_door = 'There is no door in this direction to close'
    nesw_wall = 'You cannot close a wall'
    not_found = 'There is nothing to close'

    def execute(self):
        player = self.find_player()
        room = player.character.current_room
        direction = self.determine_direction(self.payload.lower())

        # If the payload was NESW, treat this as a door
        if direction is not None:
            return self.handle_doors(room, direction, player)

        # Otherwise we need to find in the room
        return self.handle_contents(room, player, self.payload)

    def handle_contents(self, room, player, item_name):
        '''Try to find the item in the room, then run on_close on it if so'''
        item = self.find_in_room(room, item_name)
        if item is not None:
            # We found it, so run on_close on it
            return item.on_close(player)

        # Send a failure message
        return Close.not_found

    def handle_doors(self, room, direction, player):
        '''
        Treat this command as an close doors command, since the user typed in
        a direction
        '''
        in_direction = room.get_in_direction(direction)

        # No connections have been made in this direction
        if in_direction is None:
            return Close.nesw_wall

        # determine if the door prevents movement
        door = in_direction.door
        if door is None:
            # There is no door to close
            return Close.nesw_no_door

        # Have the door handle it now
        return door.on_close(player)
