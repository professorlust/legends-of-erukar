from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Containable import Containable
import random, math, erukar

class Inspect(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'
    NotEnoughAP = 'Not enough action points!'
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."
    
    NeedsArgs = False
    ActionPointCost = 2
    '''
    Requires:
        interaction_target
    '''

    def perform(self):
        if 'interaction_target' not in self.args or not self.args['interaction_target']:
            if not self.args['player_lifeform'].room: return self.fail(Inspect.NoTarget)
            self.args['interaction_target'] = self.args['player_lifeform'].room

        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Inspect.NotEnoughAP)
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)

        # Index in the player's active indexing tree
        acu, sen = self.args['player_lifeform'].lifeform().get_detection_pair()
        self.index(acu, sen)

        inspect_result = self.args['interaction_target'].on_inspect(self.args['player_lifeform'], acu, sen)
        self.append_result(self.player_info.uid, inspect_result)
        return self.succeed()

    def index(self, acu, sen):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        pass
#       if issubclass(type(container), Containable):
#           for i in container.contents:
#               player.index_item(i, container)
