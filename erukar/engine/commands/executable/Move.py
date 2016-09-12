from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment import *
import erukar

class Move(ActionCommand):
    move_through_wall = 'You attempt to pass through a wall with no luck'
    move_through_closed_door = 'You cannot move this way because a door prevents you from doing so'
    move_successful = 'You have successfully moved {0}.\n\n{1}'
    enemy_movement = '{} has moved {}.'

    def execute(self):
        player = self.find_player()
        direction = self.determine_direction(self.payload().lower())
        if direction is None: return ''
        in_direction = self.lifeform(player).current_room.get_in_direction(direction)

        # determine if the door prevents movement
        door = in_direction.door
        if door is not None:
            if type(door) is Door and door.status is not Door.Open:
                return self.fail(Move.move_through_closed_door)
            if type(door) is Surface:
                return self.fail(Move.move_through_wall)

        # Move and autoinspect the room for the player
        if in_direction.room is None:
            return self.fail(Move.move_through_wall)
        return self.succeed(self.change_room(player, in_direction.room, direction))

    def change_room(self, player, new_room, direction):
        '''Used to transfer the character from one room to the next'''
        lifeform = self.lifeform(player)
        if lifeform in lifeform.current_room.contents:
            lifeform.current_room.contents.remove(lifeform)
        lifeform.link_to_room(new_room)

        if isinstance(player, erukar.engine.model.PlayerNode):
            player.move_to_room(new_room)

            i = Inspect()
            i.data = self.data
            i.sender_uid = self.sender_uid
            inspection_result = i.execute()

            return Move.move_successful.format(direction.name, inspection_result.result)

        return Move.enemy_movement.format(lifeform.alias(), direction.name)
