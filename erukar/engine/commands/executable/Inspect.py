from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Containable import Containable
import random, math, erukar
from erukar.nlg.Environment import Environment

import logging
logger = logging.getLogger('debug')

class Inspect(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'
    NotEnoughAP = 'Not enough action points!'
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."
    
    NeedsArgs = False
    ActionPointCost = 2
    '''
    Requires:
        interaction_target
    or
        coordinates
    '''

    def perform(self):
        if 'interaction_target' not in self.args or not self.args['interaction_target']:
            self.args['interaction_target'] = self.specified_coordinates()

        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Inspect.NotEnoughAP)
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)

        room_description = Environment.describe_area(self.args['player_lifeform'], self.world, self.args['interaction_target'])
        self.append_result(self.player_info.uid, room_description)
        return self.succeed()

    def index(self, acu, sen):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        if isinstance(self.args['interaction_target'], erukar.engine.environment.Room):
            for item in self.args['interaction_target'].detected_contents(acu, sen):
                self.player_info.index_item(item, self.args['interaction_target'])
