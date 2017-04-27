from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Direction import Direction
from erukar.engine.environment import *
import erukar

class Move(ActionCommand):
    move_through_closed_door = 'You cannot move this way because a door prevents you from doing so'
    move_successful = 'You have successfully moved {0}.'
    enemy_movement = '{} has moved {}.'

    '''
    Requires:
        passage
    '''
    
    def cost_to_move(self):
        '''In the future, Larger rooms may cost more AP to move'''
        return 1

    def perform(self):
        if 'passage' not in self.args or not self.args['passage']: return self.fail('Passage not specified')
        #if self.args['passage'].door

        cost = self.cost_to_move()
        if self.args['player_lifeform'].action_points < cost:
            return self.fail('You do not have enough Action Points to move that way.')
        self.args['player_lifeform'].action_points -= cost

        new_room = self.args['passage'].next_room(self.args['player_lifeform'].room)
        return self.change_room(new_room)

    def change_room(self, new_room):
        '''Used to transfer the character from one room to the next'''

        self.args['player_lifeform'].room.remove(self.args['player_lifeform'])

        self.args['player_lifeform'].link_to_room(new_room)
        self.append_result(self.player_info.uuid, 'Move successful')

        for content in new_room.contents:
            self.inform_of_movement(content)

        if isinstance(self.player_info, erukar.engine.model.PlayerNode):
            self.move_player(new_room)
        return self.succeed()

    def inform_of_movement(self, content):
        if not hasattr(content, 'uid'): return
        
        if content.uid != self.player_info.uuid:
            self.append_result(self.player_info.uuid, 'In the new room you see {}.'.format(content.alias()))

    def move_player(self, new_room):
        self.args['player_lifeform'].move_to_room(new_room)

        i = Inspect()
        i.data = self.data
        i.sender_uid = self.player_info.uuid
        inspection_result = i.execute()
        self.append_result(self.player_info.uuid, ' '.join(inspection_result.results[self.player_info.uuid]))
