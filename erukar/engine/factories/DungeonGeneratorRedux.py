from erukar.engine.model.CoordinateTranslator import CoordinateTranslator
from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.environment import *
from erukar.engine.calculators import *
from erukar.engine.calculators.meta import AStarBase, Queue
import numpy as np
import math, random

class DungeonGeneratorRedux(FactoryBase, AStarBase):
    Small       = 8
    Medium      = 16
    Large       = 24
    Huge        = 32

    ManhattanD  = 10

    NumberOfLinearityPasses = 32
    MinimumLinearityForRisk = 4
    NumberOfOffshoots       = 10
    MinimumOffshootLength   = 2
    MaximumOffshootLength   = 5

    def __init__(self, size=24):
        self.rooms = []
        self.connections = {}
        self.size = size

    def generate(self, previous_instance_identifier=''):
        self.dungeon = Dungeon()
        room = Room(self.dungeon)
        room.walls = [Surface()]
        #self.create_dungeon()
        return self.dungeon

    def create_dungeon(self):
        self.create_rooms() 
        for room in self.rooms:
            self.randomly_connect(room)

        self.create_rooms_along_lines()
        for _ in range(self.NumberOfLinearityPasses):
            self.build_junction_based_on_linearity()
        for _ in range(self.NumberOfOffshoots):
            self.build_offshoot()
        self.fill_walls()

    def create_rooms_along_lines(self):
        '''Use the connections from the random connection process to generate A* paths and then connect'''
        visited_connections = []
        for origin in self.rooms:
            if not origin in self.connections: continue
            for destination in iter(self.connections[origin]):
                if [origin, destination] in visited_connections:
                    continue
                cf, ec = self.search(self.rooms, origin, destination)
                path = self.reverse(cf, origin, destination)
                self.add_room_path(path, origin)
                visited_connections.append([origin, destination])
                visited_connections.append([destination, origin])

    def add_room_path(self, path, origin):
        '''Use an A* Path to add a bunch of rooms from one objective to the other'''
        previous = None
        for coord in path:
            if coord not in self.dungeon.rooms:
                self.rooms.append(coord)
                current = self.dungeon.get_room_at(coord)
                if not current:
                    current = Room(self.dungeon, coord)

                if previous and previous != current:
                    direction = Navigator.direction_between(current.coordinates, previous.coordinates)
                    current.connect(previous, None)

                previous = current

    def build_offshoot(self):
        '''Build random off-shoots which go nowhere, but overall decrease linearity'''
        self.determine_linearity()
        at_risk = [x for x in self.dungeon.rooms if x.linearity > self.MinimumLinearityForRisk]
        
        #determine start randomly
        distribution = [self.linearity_weight(st) for st in self.rooms]
        coords = self.rooms[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]
        current = self.dungeon.get_room_at(coords)

        for added in range(int(random.random() * (self.MaximumOffshootLength-self.MinimumOffshootLength) + self.MinimumOffshootLength)): 
            available_rooms = list(current.wall_directions())
            if len(available_rooms) == 0: return
            direction = random.choice(available_rooms)
            new_coords = CoordinateTranslator.translate(current.coordinates, direction)
            new_room = Room(self.dungeon, new_coords)
            if not new_room.is_valid:
                break
            current.connect(new_room, None)
            current = new_room


    def build_junction_based_on_linearity(self):
        '''Attempts to build connections (junctions) between two highly linear rooms'''
        self.determine_linearity()
        at_risk = [x for x in self.dungeon.rooms if x.linearity > self.MinimumLinearityForRisk]
        
        #determine start randomly
        distribution = [self.linearity_weight(st) for st in self.rooms]
        start = self.rooms[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]

        # determine end randomly
        distribution = [self.linearity_weight(dest) * self.distance_weight(start, dest) for dest in self.rooms if dest != start]
        dest = self.rooms[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]

        cf, ec = self.search(self.rooms, start, dest)
        path = self.reverse(cf, start, dest)
        self.add_room_path(path, start)

    def get_from_unnormalized_distribution(distribution):
        distribution = [a / sum(distribution) for a in distribution]
        bins, values = Random.create_random_distribution(list(range(len(distribution))), distribution)
        return Random.get_from_custom_distribution(random.random(), bins, values)

    def determine_linearity(self):
        '''Do a single pass over the entire dungeon, calculating linearity scores'''
        calculation_queue = Queue()
        branch_points = {x for x in self.dungeon.rooms if len(list(x.adjacent_rooms())) > 2}
        branch_points.add(self.dungeon.rooms[0])
        starts_evaluated = set()
        
        for bp in iter(branch_points):
            for direction in bp.adjacent_rooms():
                if bp.connections[direction].room in starts_evaluated: continue
                self.build_and_evaluate_linear_branch(bp, direction, branch_points, starts_evaluated)

    def build_and_evaluate_linear_branch(self, origin, direction, branch_points, starts_evaluated):
        '''Iterate from an origin along a direction to find the linearity'''
        current = origin.connections[direction].room
        current_path = [origin]
        while current not in current_path:
            current_path.append(current)
            if current is None:
                self.linear_to_dead_end(current_path, starts_evaluated)
                return
            if current in branch_points:
                self.linear_to_junction(current_path, starts_evaluated)
                return

            # Get Next
            current = next((current.connections[x].room for x in current.adjacent_rooms() if current.connections[x].room not in current_path), None) 

    def linear_to_dead_end(self, current_path, starts_evaluated):
        '''Assign linearity with max at end of current path'''
        starts_evaluated.add(current_path[0])
        to_i = len(current_path) - 1
        for i in range(to_i):
            current_path[i].linearity = i

    def linear_to_junction(self, current_path, starts_evaluated):
        '''Assign linearity with max in center of current path'''
        starts_evaluated.add(current_path[0])
        starts_evaluated.add(current_path[-1])
        to_i = int(len(current_path)/2) + 1
        for i in range(to_i):
            current_path[i].linearity = i
            current_path[-i-1].linearity = i
        
    def create_rooms(self):
        '''Should be pretty straightforward'''
        num_rooms = int(np.random.beta(8, 4) * self.size)
        for i in range(num_rooms):
            new_coord = self.get_unique_coordinate()
            self.rooms.append(new_coord)

    def get_unique_coordinate(self):
        coord = (self.random_coordinate(), self.random_coordinate())
        if coord in self.rooms:
            coord = self.get_unique_coordinate()
        return coord

    def random_coordinate(self):
        return int(16*(random.random()-0.5))

    def distance_weight(self, room, destination):
        '''Creates a scalar based on the distance between two coordinates'''
        dist = Navigator.distance(room, destination)
        if dist == 0: return 0
        return 10 / math.pow(dist, 2)

    def connection_weight(self, room):
        '''Creates a scalar based on the number of existing connections at a room'''
        if room not in self.connections:    return 10
        if len(self.connections[room]) > 3: return 0
        return 5 / math.pow(len(self.connections[room]), 2)

    def collision_weight(self, start, dest):
        '''Check if there's a collision -- if so, reduce the probability to 0'''
        for other_start in self.connections:
            for other_dest in self.connections[other_start]:
                if Navigator.intersects(start, dest, other_start, other_dest):
                    return 0
        return 1

    def linearity_weight(self, coords):
        '''Used to greatly sway linearity adjustments'''
        room = self.dungeon.get_room_at(coords)
        return 0 if not room else math.pow(room.linearity, 2)

    def randomly_connect(self, for_room):
        '''Connect a room a random number of times to random rooms'''
        connections_remaining = 4 - self.number_of_connections(for_room)
        number_of_times_to_connect = int(random.random() * (connections_remaining-1))+1
        for i in range(number_of_times_to_connect):
            self.do_connection(for_room)

    def do_connection(self, for_room):
        '''Randomly determines which room that the passed-in room should connect to, then does it'''
        distribution = [self.connection_weight(dest) * self.distance_weight(for_room, dest) * self.collision_weight(for_room, dest) for dest in self.rooms]
        # Normalize
        if sum(distribution) == 0:
            return
        distribution = [a / sum(distribution) for a in distribution]
        bins, values = Random.create_random_distribution(list(range(len(distribution))), distribution)
        result = Random.get_from_custom_distribution(random.random(), bins, values)
        # Actually add the room connections
        self.add_connection(for_room, self.rooms[result])
        self.add_connection(self.rooms[result], for_room)

    def add_connection(self, for_room, dest):
        '''Add a connection to the set tied to the passed-in room'''
        if for_room not in self.connections:
            self.connections[for_room] = {dest}
        else:
            self.connections[for_room].add(dest)

    def number_of_connections(self, for_room):
        '''Returns the number of connected rooms to the passed-in room'''
        if for_room not in self.connections:
            return 0
        return len(self.connections[for_room])

    def fill_walls(self):
        '''Fill in the abyss with walls (ugly, need to optimize)'''
        for room in self.dungeon.rooms:
            for direction in room.wall_directions():
                room.connections[direction] = Passage(wall=Surface())

    '''AStarBase stuff'''
    def heuristic(self, node, goal):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return self.ManhattanD * (dx+dy)

    def neighbors(self, collection, node, goal):
        possibilities = [
            (node[0]-1, node[1]),
            (node[0]+1, node[1]),
            (node[0],   node[1]-1),
            (node[0],   node[1]+1),
        ]
        p = [x for x in possibilities if (x not in self.rooms or x == goal) and -10 < x[0] < 10 and -10 < x[1] < 10]
        return p

    def cost(self, collection, current, node):
        return 1
