from erukar.engine.factories.FactoryBase import FactoryBase
from erukar.engine.calculators import *
import numpy as np
import math, random

class DungeonGeneratorRedux(FactoryBase):
    def __init__(self):
        self.rooms = []
        self.connections = {}

    def generate(self, previous_instance_identifier=''):
        self.dungeon = Dungeon()
        self.create_dungeon()
        

    def create_dungeon(self):
        self.create_rooms() 
        for room in self.rooms:
            self.randomly_connect(room)

    def create_rooms(self):
        '''Should be pretty straightforward'''
        num_rooms = int(np.random.beta(8, 4) * 32)
        for i in range(num_rooms):
            new_coord = self.get_unique_coordinate()
            self.rooms.append(new_coord)

    def get_unique_coordinate(self):
        coord = (self.random_coordinate(), self.random_coordinate())
        if coord in self.rooms:
            coord = self.get_unique_coordinate()
        return coord

    def random_coordinate(self):
        return int(20*(random.random()-0.5))

    def determine_branches(self):
        ''''''
        # constants for determining branch destination
        ChanceToContinueBranch  = 0.6
        ChanceToJoinOtherBranch = 0.3
        ChanceToEndBranch       = 0.1

    def distance_value(self, room, destination):
        '''Creates a scalar based on the distance between two coordinates'''
        dist = Navigator.distance(room, destination)
        if dist == 0: return 0
        return 10 / math.pow(dist, 2)

    def connection_value(self, room):
        '''Creates a scalar based on the number of existing connections at a room'''
        if room not in self.connections:    return 10
        if len(self.connections[room]) > 3: return 0
        return 5 / math.pow(len(self.connections[room]), 2)

    def collision_value(self, start, dest):
        for other_start in self.connections:
            for other_dest in self.connections[other_start]:
                if Navigator.intersects(start, dest, other_start, other_dest):
                    return 0
        return 1

    def randomly_connect(self, for_room):
        connections_remaining = 4 - self.number_of_connections(for_room)
        number_of_times_to_connect = int(random.random() * (connections_remaining-1))+1
        for i in range(number_of_times_to_connect):
            self.do_connection(for_room)

    def do_connection(self, for_room):
        distribution = [self.connection_value(dest) * self.distance_value(for_room, dest) * self.collision_value(for_room, dest) for dest in self.rooms]
        # Normalize
        if sum(distribution) == 0:
            return
        distribution = [a / sum(distribution) for a in distribution]
        bins, values = Random.create_random_distribution(list(range(len(distribution))), distribution)
        result = Random.get_from_custom_distribution(random.random(), bins, values)
        self.add_connection(for_room, self.rooms[result])
        self.add_connection(self.rooms[result], for_room)

    def add_connection(self, for_room, dest):
        if for_room not in self.connections:
            self.connections[for_room] = {dest}
        else:
            self.connections[for_room].add(dest)

    def number_of_connections(self, for_room):
        if for_room not in self.connections:
            return 0
        return len(self.connections[for_room])
