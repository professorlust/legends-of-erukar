from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.ActionCommand import ActionCommand
from erukar.engine.calculators.Pathing import Pathing
import erukar, math

class Move(ActionCommand):
    move_through_closed_door = 'You cannot move this way because a door prevents you from doing so'
    move_successful = 'You have successfully moved {0}.'
    enemy_movement = '{} has moved {}.'

    '''
    Requires:
        coordinates
    '''
    
    def cost_to_move(self, path):
        '''
        Use A* to figure out the distance from where we are to the new coordinates
        If the path is inaccessible (either because the fog of war has not revealed that
        area or there is just no path to it), this should return -1
        '''
        if len(path) < 2: return -1
        total_move_distance = len(path) - 1
        return math.ceil(total_move_distance / self.args['player_lifeform'].move_speed())

    def get_path_to(self, coordinates):
        start = self.args['player_lifeform'].coordinates
        goal = coordinates
        collection = list(self.world.all_traversable_coordinates())
        
        pather = Pathing(collection)
        path_info, cost = pather.search(collection, start, goal)
        path = pather.reverse(path_info, start, goal)
        if path: path.pop(0)
        return path

    def perform(self):
        if 'coordinates' not in self.args or not self.args['coordinates']:
            return self.fail('No coordinates found')

        self.args['coordinates'] = self.specified_coordinates()

        path = self.get_path_to(self.args['coordinates'])
        cost = self.cost_to_move(path)
        if cost == -1: 
            return self.fail('A path could not be found to reach {}'.format(self.args['coordinates']))
        if self.args['player_lifeform'].action_points() < cost:
            return self.fail('You do not have enough Action Points to move that way.')
        self.args['player_lifeform'].consume_action_points(cost)

        return self.do_move(path)

    def do_move(self, path):
        '''Here we move over each coordinate, allowing others the chance to see us and giving
        ourselves the ability to see things as we go. It's also rather insidious, as it 
        potentially forces us '''
        while len(path) > 0:
            self.args['player_lifeform'].on_move(path.pop(0))
        return self.succeed()
