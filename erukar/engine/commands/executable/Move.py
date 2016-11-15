from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.environment import *
import erukar

class Move(ActionCommand):
    move_through_wall = 'You attempt to pass through a wall with no luck'
    move_through_closed_door = 'You cannot move this way because a door prevents you from doing so'
    move_successful = 'You have successfully moved {0}.'
    enemy_movement = '{} has moved {}.'

    aliases = ['move']
    TrackedParameters = ['direction']

    def execute(self):
        player = self.find_player().lifeform()
        failure = self.check_for_arguments()
        if failure: return failure

        in_direction = player.current_room.get_in_direction(self.direction)

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
        self.change_room(self.find_player(), in_direction.room)
        return self.succeed()

    def resolve_direction(self, opt_payload=''):
        # If this is on the context, grab it and return
        if self.context and self.context.should_resolve(self):
            self.target = getattr(self.context, 'target')

        # If we have the parameter and it's not nully, assert that we're done
        if hasattr(self, 'target') and self.target: return

        self.direction = self.determine_direction(opt_payload.lower())
        if self.direction:
            return
        return self.fail('"{}" is not an acceptable direction.'.format(opt_payload))

    def change_room(self, player, new_room):
        '''Used to transfer the character from one room to the next'''
        lifeform = self.lifeform(player)
        if lifeform in lifeform.current_room.contents:
            lifeform.current_room.contents.remove(lifeform)
        lifeform.link_to_room(new_room)
        self.append_result(self.sender_uid, Move.move_successful.format(self.direction.name))

        for content in new_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not lifeform:
                self.append_result(content.uid, '{} has moved {}.'.format(lifeform.alias(), self.direction.name))

        if isinstance(player, erukar.engine.model.PlayerNode):
            player.move_to_room(new_room)

            i = Inspect()
            i.data = self.data
            i.sender_uid = self.sender_uid
            inspection_result = i.execute()
            self.append_result(self.sender_uid, ' '.join(inspection_result.results[self.sender_uid]))
