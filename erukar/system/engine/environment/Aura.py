from erukar.system.engine import Describable
from erukar.ext.math import Navigator, Distance
import math


class Aura(Describable):
    BriefDescription = "You feel an aura originating from the {rel_direction}."
    SelfAuraDescription = "You sense your own aura."

    def __init__(self, location, strength=2, max_distance=6):
        '''
        An aura can only affect if its strength is >= 1. In the defaults, the
        aura's strength of 2 and decay of 0.5 mean that it has a strength of
        2 at the origin, 1 in adjacent rooms, and cannot affect outside of
        these tiles.
        '''
        super().__init__()
        self.initiator = None
        self.location = location
        self.aura_strength = strength
        self.max_distance = max_distance
        self.blocked_by_walls = False
        self.is_expired = False
        self.needs_rebuilt = True

    def rebuild_affected_tiles(self):
        self.needs_rebuilt = False
        coords = self.world.all_traversable_coordinates()
        circle = Distance.direct_los(self.location, coords, self.max_distance)
        self.affected_tiles = set(circle)

    def strength_at(self, loc):
        dist = math.ceil(self.distance(loc))
        if dist > self.max_distance:
            return 0
        normalizer = math.log10(self.max_distance + 1)
        scalar = math.log10(1 + self.max_distance - dist)
        return scalar * self.aura_strength / normalizer

    def move(self, loc):
        self.needs_rebuilt = self.location != loc
        self.location = loc

    def affects_tile(self, loc):
        '''This is used for the quick calculations for the dungeon'''
        if self.needs_rebuilt:
            self.rebuild_affected_tiles()
        return loc in self.affected_tiles

    def distance(self, to_coordinate):
        return Navigator.distance(self.location, to_coordinate)

    def directionality(self, from_coordinate):
        if from_coordinate == self.location:
            return 'this area'

        angle = Navigator.angle(from_coordinate, self.location)
        direction = Navigator.angle_to_direction(angle)

        return 'the {}'.format(direction.name.lower())

    def tick(self):
        '''
        Time-based, regular Tick that occurs every 25 ticks in a TurnManager
        (5 seconds). For time-based auras, this might decrement a timer
        function. If that timer is at zero at the end, it sets the expired flag
        to true, then is removed by the dungeon on the next cleanup cycle
        '''
        pass
