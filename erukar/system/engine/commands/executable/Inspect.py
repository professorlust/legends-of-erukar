from ..ActionCommand import ActionCommand
from erukar.ext.nlg import Environment
from erukar.ext.math import Distance


class Inspect(ActionCommand):
    NoTarget = 'Unable to locate interaction_target'
    NotEnoughAP = 'Not enough action points!'
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
        self.args['interaction_target'] = getattr(
            self.args,
            'interaction_target',
            self.specified_coordinates())

        cost = self.ActionPointCost
        if self.args['player_lifeform'].action_points() < cost:
            return self.fail(Inspect.NotEnoughAP)
        self.args['player_lifeform'].consume_action_points(cost)

        self.perform_inspection()
        self.inspect_sanctity()
        return self.succeed()

    def perform_inspection(self):
        player = self.args['player_lifeform']
        acu, sen = player.get_detection_pair()
        acu *= (1.0 - self.ObservationPenalty)
        sen *= (1.0 - self.ObservationPenalty)

        origin = player.coordinates
        open_space = self.world.all_traversable_coordinates()
        at = self.args['interaction_target']
        max_range = self.FogOfWarScalar * player.visual_fog_of_war()

        visual_area = list(Distance.direct_los(
            origin,
            open_space,
            max_range,
            at,
            self.RadiusAroundInspection))

        player.detect_in_area(visual_area)

        room_description = Environment.describe_area_visually(
            player, acu, sen,
            self.world, visual_area)

        self.append_result(self.player_info.uid, room_description)

    def inspect_sanctity(self):
        loc = self.args['interaction_target']
        sanctity = self.world.sanctity_at(loc)
        if sanctity < -0.3:
            self.append_result(self.player_info.uid, 'This area is demonic.')
        elif sanctity > 0.3:
            self.append_result(self.player_info.uid, 'This area feels sacred.')
