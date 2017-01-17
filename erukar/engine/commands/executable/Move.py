from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Direction import Direction
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
        failure = self.check_for_arguments()
        if failure: return failure

        return self.attempt_move()

    def attempt_move(self):
        in_direction = self.room.get_in_direction(self.direction)

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
        self.change_room(in_direction.room)
        return self.succeed()

    def change_room(self, new_room):
        '''Used to transfer the character from one room to the next'''
        if self.lifeform in self.room.contents:
            self.room.contents.remove(self.lifeform)
        self.lifeform.link_to_room(new_room)
        self.append_result(self.sender_uid, Move.move_successful.format(self.direction.name))

        for content in new_room.contents:
            self.inform_of_movement(content)

        if isinstance(self.player, erukar.engine.model.PlayerNode):
            self.move_player(new_room)

    def inform_of_movement(self, content):
        if not hasattr(content, 'uid'): return
        
        if content.uid != self.sender_uid:
            print('Telling {} that {} has moved'.format(content.uid, self.sender_uid))
            self.append_result(content.uid, '{} has moved {}.'.format(self.lifeform.alias(), self.direction.name))
            self.append_result(self.sender_uid, 'In the new room you see {}.'.format(content.alias()))

    def move_player(self, new_room):
        self.player.move_to_room(new_room)

        i = Inspect()
        i.data = self.data
        i.sender_uid = self.sender_uid
        inspection_result = i.execute()
        self.append_result(self.sender_uid, ' '.join(inspection_result.results[self.sender_uid]))
