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
    or
        coordinates
    '''

    def perform(self):
        if 'interaction_target' not in self.args or not self.args['interaction_target']:
            coords = self.specified_coordinates()
            room = self.world.get_room_at(coords)
            self.args['interaction_target'] = room

        if self.args['player_lifeform'].action_points() < self.ActionPointCost:
            return self.fail(Inspect.NotEnoughAP)
        self.args['player_lifeform'].consume_action_points(self.ActionPointCost)

        # Index in the player's active indexing tree
        acu, sen = self.args['player_lifeform'].lifeform().get_detection_pair()
        self.index(acu, sen)

#       inspect_result = self.args['interaction_target'].on_inspect(self.args['player_lifeform'], acu, sen)
#       self.append_result(self.player_info.uid, inspect_result)
        self.visible_actors(acu, sen)
        return self.succeed()

    def index(self, acu, sen):
        '''Indexes all items in a container for the PlayerNode's indexer'''
        if isinstance(self.args['interaction_target'], erukar.engine.environment.Room):
            for item in self.args['interaction_target'].detected_contents(acu, sen):
                self.player_info.index_item(item, self.args['interaction_target'])

    def visible_actors(self, acu, sen):
        view_distance = 3
        for actor in self.world.actors_in_range(self.args['player_lifeform'].coordinates, view_distance):
            self.append_result(self.player_info.uid, actor.on_inspect(self.args['player_lifeform'], acu, sen))
