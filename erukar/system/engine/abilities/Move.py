from erukar.system.engine import TargetedAbility
from erukar.ext.math import Pathing


class Move(TargetedAbility):
    Name = "Move"
    ShowInLists = False
    Description = 'Move to {}'

    def valid_at(self, cmd, loc):
        ap = cmd.args['player_lifeform'].action_points()
        return 0 < self.ap_cost(cmd, loc) <= ap

    def action_for_map(self, cmd, loc):
        yield {
            'command': 'ActivateAbility',
            'abilityModule': self.__module__,
            'cost': self.ap_cost(cmd, loc),
            'description': self.format_description(cmd, loc)
        }

    def ap_cost(self, cmd, loc):
        costs = list(Move.costs(cmd.args['player_lifeform'], *loc))
        if not costs or len(costs) == 0:
            return -1
        return min(costs)

    def costs(player, x, y):
        moveset = player.zones.movement
        for cost in moveset:
            if (x, y) in moveset[cost]:
                yield cost

    def format_description(self, cmd, loc):
        loc_str = '({}, {})'.format(*loc)
        return self.Description.format(loc_str)

    def get_path_to(cmd, loc):
        start = cmd.args['player_lifeform'].coordinates
        collection = list(cmd.world.all_traversable_coordinates())

        pather = Pathing(collection)
        path_info, cost = pather.search(collection, start, loc)
        path = pather.reverse(path_info, start, loc)
        if path:
            path.pop(0)
        return path

    def perform(self, cmd):
        if not cmd.args.get('coordinates'):
            return cmd.fail('No coordinates found')
        loc = cmd.specified_coordinates()
        cost = self.ap_cost(cmd, loc)
        if cost == -1:
            fail_str = 'A path could not be found to reach {}'
            return cmd.fail(fail_str.format(loc))
        if cmd.args['player_lifeform'].action_points() < cost:
            fail_str = 'You do not have enough Action Points to move that way.'
            return cmd.fail(fail_str)
        cmd.args['player_lifeform'].consume_action_points(cost)
        path = Move.get_path_to(cmd, loc)
        Move.do_move(cmd, path)
        return cmd.succeed()

    def do_move(cmd, path):
        '''Here we move over each coordinate, allowing others the chance to
        see us and giving ourselves the ability to see things as we go. It's
        also rather insidious, as it potentially forces us '''
        player = cmd.args['player_lifeform']
        start = player.coordinates
        final = path[-1]
        move_str = 'You move from {} to {}'.format(start, final)
        cmd.append_result(player.uid, move_str)
        player.on_move(final)
        detected_str = 'You see {} move to {} from {}.'.format(
            player.alias(), start, final)
        for lf in cmd.world.sentient_actors(player):
            if lf.can_detect(player):
                lf.detected_entities.add(player)
                cmd.append_result(lf.uid, detected_str)
