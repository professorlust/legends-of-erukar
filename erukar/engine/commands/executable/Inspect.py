from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.model.Containable import Containable
import random, math, erukar
from erukar.nlg.Environment import Environment
from erukar.engine.calculators.Distance import Distance

class Inspect(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'
    NotEnoughAP = 'Not enough action points!'
    abyss = "There is nothing to your {0} except the abyss... plain and nothingness forever."
    
    NeedsArgs = False
    ActionPointCost = 2

    RadiusAroundInspection = 5
    FogOfWarScalar = 2.0
    ObservationPenalty = 0.00
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

        self.perform_inspection()
        return self.succeed()
    
    def perform_inspection(self):
        acu, sen = self.args['player_lifeform'].get_detection_pair()
        acu *= (1.0 - self.ObservationPenalty)
        sen *= (1.0 - self.ObservationPenalty)

        origin = self.args['player_lifeform'].coordinates
        open_space = self.world.all_traversable_coordinates()
        at = self.args['interaction_target']
        max_range = self.FogOfWarScalar * self.args['player_lifeform'].visual_fog_of_war()
        visual_area = list(Distance.direct_los(origin, open_space, max_range, at, self.RadiusAroundInspection))
        for loc in visual_area:
            self.args['player_lifeform'].zones.all_seen.add(loc)

        room_description = Environment.describe_area_visually(self.args['player_lifeform'], acu, sen, self.world, visual_area)
        self.append_result(self.player_info.uid, room_description)
