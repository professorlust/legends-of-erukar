from ..ActionCommand import ActionCommand
import math


class Movea(ActionCommand):
    move_successful = 'You have successfully moved {0}.'
    enemy_movement = '{} has moved {}.'
    RebuildZonesOnSuccess = True

    '''
    Requires:
        coordinates
    '''

    def perform(self):
        if 'coordinates' not in self.args or not self.args['coordinates']:
            return self.fail('No coordinates found')

        self.args['coordinates'] = self.specified_coordinates()

        path = self.get_path_to(self.args['coordinates'])
        cost = self.cost_to_move(path)
        if cost == -1:
            fail_str = 'A path could not be found to reach {}'
            return self.fail(fail_str.format(self.args['coordinates']))
        if self.args['player_lifeform'].action_points() < cost:
            fail_str = 'You do not have enough Action Points to move that way.'
            return self.fail(fail_str)
        self.args['player_lifeform'].consume_action_points(cost)

        return self.do_move(path)

    def cost_to_move(self, path):
        '''
        Use A* to figure out the distance from where we are to the new
        coordinates. If the path is inaccessible (either because the
        fog of war has not revealed that area or there is just no path
        to it), this should return -1
        '''
        if len(path) < 2:
            return -1
        total_move_distance = len(path) - 1
        speed = self.args['player_lifeform'].move_speed()
        return math.ceil(total_move_distance / speed)

    def get_path_to(self, coordinates):
        start = self.args['player_lifeform'].coordinates
        goal = coordinates
        collection = list(self.world.all_traversable_coordinates())

        pather = Pathing(collection)
        path_info, cost = pather.search(collection, start, goal)
        path = pather.reverse(path_info, start, goal)
        if path:
            path.pop(0)
        return path

    def do_move(self, path):
        '''Here we move over each coordinate, allowing others the chance to
        see us and giving ourselves the ability to see things as we go. It's
        also rather insidious, as it potentially forces us '''
        player = self.args['player_lifeform']
        start = player.coordinates
        final = path[-1]
        move_str = 'You move from {} to {}'.format(start, final)
        self.append_result(player.uid, move_str)
        player.on_move(final)
        detected_str = 'You see {} move to {} from {}.'.format(
            player.alias(), final, start)
        for lf in self.world.sentient_actors(player):
            if lf.can_detect(player):
                lf.detected_entities.add(player)
                self.append_result(lf.uid, detected_str)
        return self.succeed()
