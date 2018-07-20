from erukar.system.engine import Range, Dungeon, Wall, Room, TransitionPiece, OverlandZone
from .FactoryBase import FactoryBase
from .EnemyGenerator import EnemyGenerator
from .ModuleDecorator import ModuleDecorator
from .TileGenerator import TileGenerator
from .ModifierGenerator import ModifierGenerator
from erukar.ext.math import *
from erukar.ext.math.aux import AStarBase, Queue
import math, random, erukar, numpy, sys, inspect

class DungeonGenerator(FactoryBase, AStarBase):
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

    MaxHeight = 15
    MaxWidth = 15

    def __init__(self, location, size=24):
        self.location = location
        self.environment_profile = location.environment_profile
        self.vertices = []
        self.connections = {}
        self.size = size
        self.potential_floor_tiles = [
            erukar.content.Cobblestone(),
            erukar.content.Dirt(),
            erukar.content.Sand(),
            erukar.content.Snow(),
            erukar.content.StoneFloor(),
            erukar.content.Grass(),
            erukar.content.FrozenGrass(),
            erukar.content.Tiles()
        ]
        self.potential_wall_tiles = [
            erukar.content.Pine(),
            erukar.content.StoneWall(),
            erukar.content.StoneBricks(),
            erukar.content.SandStoneBricks()
        ]

    def generate(self, previous_instance_identifier='', override_type=None):
        self.create_dungeon(override_type)

        self.enemy_generator = EnemyGenerator(self)
        self.enemy_generator.add_enemies()
        self.add_items()

        self.add_transitions()
        self.world.spawn_coordinates = self.vertices
        self.world.location = self.location
        return self.world

    def create_dungeon(self, override_type=None):
        self.world = (override_type or (
            OverlandZone if self.location.use_day_night_cycle else Dungeon
        ))()
        self.world.base_ambient_light = self.location.ambient_light
        self.create_vertices()
        for vertex in self.vertices:
            self.connect_to_random_vertex(vertex)

        self.create_rooms_along_lines()
        self.add_floor_tiles()
        self.place_chunks_on_random_vertices()
        self.add_walls()
        self.world.generate_tiles(TileGenerator(
            width=self.world.pixels_per_side,
            breadth=self.world.pixels_per_side
        ))

    def add_enemies(self):
        enemy_chooser = ModuleDecorator('erukar.content.enemies', self.environment_profile)
        for _ in range(random.choice([2,3,3,4,4,5])):
            self.world.add_actor(enemy_chooser.create_one(), self.random_location())

    def add_items(self):
        possibilities = [
            erukar.content.inventory.ammunition.Arrow,
            erukar.content.inventory.ammunition.CrossbowBolt,
            erukar.content.inventory.consumables.Candle,
            erukar.content.inventory.PotionOfRenewal,
            erukar.content.inventory.PotionOfHealing,
            erukar.content.inventory.PotionOfGreaterHealing,
            erukar.content.inventory.consumables.Torch,
        ]
        possibilities += [x for _,x in inspect.getmembers(sys.modules['erukar.content.inventory.weapons.standard'], inspect.isclass)]
        possibilities += [x for _,x in inspect.getmembers(sys.modules['erukar.content.inventory.armor'], inspect.isclass)]

        for _ in range(random.choice([2,3,3,4,4,5])):
            item = random.choice(possibilities)
            if issubclass(item, erukar.engine.Ammunition)\
               or issubclass(item, erukar.engine.Weapon)\
               or issubclass(item, erukar.engine.Armor):
                self.add_item(item)
                continue
            self.world.add_actor(item(), self.random_location())

    def add_item(self, item_type):
        item = item_type()
        material_gen = ModifierGenerator(
            item=item,
            environment=self.environment_profile,
            module='erukar.content.modifiers.material')
        material_gen.create_one().apply_to(item)
        modifier_gen = ModifierGenerator(
            item=item,
            environment=self.environment_profile)
        while random.random() < 0.4:
            modifier_gen.create_one().apply_to(item)
        if isinstance(item, erukar.engine.Ammunition):
            item.quantity = random.randint(3,20)
        self.world.add_actor(item, self.random_location())
        self.world.add_actor_tiles(item)

    def random_location(self):
        return random.choice(self.vertices)

    def add_transitions(self):
        center = self.calculate_center()

        for coord in self.location.adjacent_sectors():
            direction = self.location.direction_to(coord)
            transition_piece = TransitionPiece(self.location.coordinates(), coord)
            transition_coord = getattr(self, direction)(center)
            self.world.add_transition(transition_piece, transition_coord)

    def calculate_center(self):
        '''Moved this to be more explicit because the generator did not read well'''
        max_x = max([coord[0] for coord in self.vertices])
        max_y = max([coord[1] for coord in self.vertices])
        min_x = min([coord[0] for coord in self.vertices])
        min_y = min([coord[1] for coord in self.vertices])

        center_x = max_x + min_x/2
        center_y = max_y + min_y/2
        return (center_x, center_y)

    def central(self, center):
        return self.get_closest_tile_to(center)

    def northeastern(self, center):
        center = center[0] + 100, center[1] + 100
        return self.get_closest_tile_to(center)

    def northwestern(self, center):
        center = center[0] - 100, center[1] + 100
        return self.get_closest_tile_to(center)

    def southeastern(self, center):
        center = center[0] + 100, center[1] - 100
        return self.get_closest_tile_to(center)

    def southwestern(self, center):
        center = center[0] - 100, center[1] - 100
        return self.get_closest_tile_to(center)

    def eastern(self, center):
        center = center[0] + 100, center[1]
        return self.get_closest_tile_to(center)

    def western(self, center):
        center = center[0] - 100, center[1]
        return self.get_closest_tile_to(center)

    def get_closest_tile_to(self, center):
        return sorted(self.vertices, key=lambda y: math.sqrt((y[0]-center[0])**2 + (y[1]-center[1])**2))[0]

    def get_floor_tile(self):
        return self.get_tile(self.potential_floor_tiles)

    def get_wall_tile(self):
        return self.get_tile(self.potential_wall_tiles)

    def get_tile(self, collection):
        weights = [tile.generation_parameters.stochasticity_weight(self.environment_profile) for tile in collection]
        bins, values = Random.create_random_distribution(collection, weights, 0)
        return Random.get_from_custom_distribution(random.random(), bins, values)

    def add_floor_tiles(self):
        for loc in self.world.all_traversable_coordinates():
            material = self.get_floor_tile()
            self.world.tiles[loc] = material

    def place_chunks_on_random_vertices(self):
        used_vertices = []
        for chunk in self.location.chunks:
            vertex = random.choice([x for x in self.vertices if x not in used_vertices])
            chunk.generate(vertex, self.world)
            self.vertices = [v for v in self.vertices if v in self.world.dungeon_map]
            if len(self.vertices) <= 1: return
            used_vertices.append(vertex)

    def add_walls(self):
        xo, yo = map(min, zip(*self.world.dungeon_map))
        xf, yf = map(max, zip(*self.world.dungeon_map))
        for y in range(yo-1, yf+2):
            for x in range(xo-1, xf+2):
                if (x,y) not in self.world.dungeon_map:
                    self.world.walls[(x, y)] = Wall()
        for loc in self.world.walls.keys():
            material = self.get_wall_tile()
            self.world.walls[loc].material = material
            if loc in self.world.tiles: continue
            self.world.tiles[loc] = material

    def create_rooms_along_lines(self):
        '''Use the connections from the random connection process to generate A* paths and then connect'''
        visited_connections = []
        for origin in self.vertices:
            if not origin in self.connections: continue
            for destination in iter(self.connections[origin]):
                # Don't Re-Add a connection
                if [origin, destination] in visited_connections: continue
                # A* search for the path
                cf, ec = self.search(self.vertices, origin, destination)
                path = self.reverse(cf, origin, destination)
                self.add_room_path(path, origin)
                visited_connections.append([origin, destination])
                visited_connections.append([destination, origin])

    def add_room_path(self, path, origin):
        '''Use an A* Path to add a bunch of rooms from one objective to the other'''
        actual_coords = [x for x in path if x not in self.world.rooms]
        new_room = Room(self.world, actual_coords)
        for coord in actual_coords: self.vertices.append(coord)
#       previous = None
#       for coord in path:
#           if coord not in self.world.rooms:
#               self.rooms.append(coord)
#               current = self.world.get_room_at(coord)
#               if not current:
#                   current = Room(self.world, coord)
#               previous = current

    def build_offshoot(self):
        '''Build random off-shoots which go nowhere, but overall decrease linearity'''
        self.determine_linearity()
        at_risk = [x for x in self.world.rooms if x.linearity > self.MinimumLinearityForRisk]
        
        #determine start randomly
        distribution = [self.linearity_weight(st) for st in self.rooms]
        coords = self.rooms[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]
        current = self.world.get_room_at(coords)

        for added in range(int(random.random() * (self.MaximumOffshootLength-self.MinimumOffshootLength) + self.MinimumOffshootLength)): 
            available_rooms = list(current.wall_directions())
            if len(available_rooms) == 0: return
            direction = random.choice(available_rooms)
            new_coords = CoordinateTranslator.translate(current.coordinates, direction)
            new_room = Room(self.world, new_coords)
            if not new_room.is_valid:
                break
            current = new_room

    def build_junction_based_on_linearity(self):
        '''Attempts to build connections (junctions) between two highly linear rooms'''
        self.determine_linearity()
        at_risk = [x for x in self.world.rooms if x.linearity > self.MinimumLinearityForRisk]
        
        #determine start randomly
        distribution = [self.linearity_weight(st) for st in self.vertices]
        start = self.vertices[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]

        # determine end randomly
        distribution = [self.linearity_weight(dest) * self.distance_weight(start, dest) for dest in self.vertices if dest != start]
        dest = self.vertices[DungeonGeneratorRedux.get_from_unnormalized_distribution(distribution)]

        cf, ec = self.search(self.vertices, start, dest)
        path = self.reverse(cf, start, dest)
        self.add_room_path(path, start)

    def get_from_unnormalized_distribution(distribution):
        distribution = [a / sum(distribution) for a in distribution]
        bins, values = Random.create_random_distribution(list(range(len(distribution))), distribution)
        return Random.get_from_custom_distribution(random.random(), bins, values)

    def determine_linearity(self):
        '''Do a single pass over the entire dungeon, calculating linearity scores'''
        calculation_queue = Queue()
        branch_points = {x for x in self.world.rooms if len(list(x.adjacent_rooms())) > 2}
        branch_points.add(self.world.rooms[0])
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
        
    def create_vertices(self):
        '''Should be pretty straightforward'''
        num_rooms = int(numpy.random.beta(8, 4) * self.size)
        for i in range(num_rooms):
            new_coord = self.get_new_unique_vertex()
            self.vertices.append(new_coord)

    def get_new_unique_vertex(self):
        coord = (self.random_coordinate(), self.random_coordinate())
        if coord in self.vertices:
            coord = self.get_new_unique_vertex()
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
        room = self.world.get_room_at(coords)
        return 0 if not room else math.pow(room.linearity, 2)

    def connect_to_random_vertex(self, origin):
        '''Connect a room a random number of times to random rooms'''
        connections_remaining = 4 - self.number_of_connections(origin)
        number_of_times_to_connect = int(random.random() * (connections_remaining-1))+1
        for i in range(number_of_times_to_connect):
            self.do_connection(origin)

    def do_connection(self, origin):
        '''Randomly determines which room that the passed-in room should connect to, then does it'''
        distribution = [self.connection_weight(v) * self.distance_weight(origin, v) * self.collision_weight(origin, v) for v in self.vertices]
        # Normalize
        if sum(distribution) == 0: return
        distribution = [a / sum(distribution) for a in distribution]
        bins, values = Random.create_random_distribution(list(range(len(distribution))), distribution)
        result = Random.get_from_custom_distribution(random.random(), bins, values)
        # Actually add the room connections
        self.add_connection(origin, self.vertices[result])
        self.add_connection(self.vertices[result], origin)

    def add_connection(self, origin, dest):
        '''Add a connection to the set tied to the passed-in room'''
        if origin not in self.connections:
            self.connections[origin] = {dest}
        else:
            self.connections[origin].add(dest)

    def number_of_connections(self, for_vertex):
        '''Returns the number of connected rooms to the passed-in room'''
        if for_vertex not in self.connections:
            return 0
        return len(self.connections[for_vertex])

    def fill_walls(self):
        '''Fill in the abyss with walls (ugly, need to optimize)'''
        for room in self.world.rooms:
            for direction in room.wall_directions():
                room.connections[direction] = Passage(wall=Surface())

    '''AStarBase stuff'''
    def heuristic(self, node, goal):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return self.ManhattanD * (dx+dy)

    def neighbors(self, collection, node, goal):
        possibilities = Neighbors.cross_pattern(node)
        p = [x for x in possibilities if (x not in self.vertices or x == goal) and -10 < x[0] < 10 and -10 < x[1] < 10]
        return p

    def cost(self, collection, current, node):
        return 1
