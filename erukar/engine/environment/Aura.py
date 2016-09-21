from erukar.engine.model.Direction import Direction
from erukar.engine.model.Describable import Describable
from erukar.engine.calculators.Navigator import Navigator
import math, operator

class Aura(Describable):
    BriefDescription = "You feel an aura originating from the {relative_direction}."

    def __init__(self, location, strength=2, decay_factor=0.5):
        '''
        An aura can only affect if its strength is >= 1. In the defaults, the aura's
        strength of 2 and decay of 0.5 mean that it has a strength of 2 at the origin,
        1 in adjacent rooms, and cannot affect outside of these tiles.
        '''
        super().__init__()
        self.location = location
        self.aura_strength = strength
        self.decay_factor = decay_factor
        self.blocked_by_walls = False
        self.is_expired = False

    def affects_tile(self, tile):
        '''This is used for the quick calculations for the dungeon'''
        dist = math.ceil(self.distance(tile.coordinates))
        strength_at_tile = self.aura_strength * math.pow(self.decay_factor, dist)
        if strength_at_tile < 1:
            return False
        if self.blocked_by_walls:
            return Navigator.exists_obstruction_between(self.location, tile)
        return True

    def distance(self, to_coordinate):
        return math.sqrt(sum(math.pow(a-b, 2) for a,b in zip(self.location.coordinates, to_coordinate)))

    def directionality(self, from_coordinate):
        if from_coordinate == self.location.coordinates:
            return 'this area'

        angle = Navigator.angle(self.location.coordinates, from_coordinate)

        # todo: rewrite 
        if math.pi/4 <= angle < 3*math.pi/4:
            return 'the north'
        if 3*math.pi/4 <= angle < 5*math.pi/4:
            return 'the west'
        if 5*math.pi/4 <= angle < 7*math.pi/4:
            return 'the south'
        return 'the east'

    def describe_brief(self, lifeform, acuity, sense):
        loc = self.directionality(lifeform.current_room.coordinates)
        return self.mutate(self.BriefDescription, {'relative_direction':loc})

    def tick(self):
        '''
        Time-based, regular Tick that occurs every 25 ticks in a TurnManager (5 seconds).
        For time-based auras, this might decrement a timer function. If that timer is at 
        zero at the end, it sets the expired flag to true, then is removed by the dungeon 
        on the next cleanup cycle
        '''
        pass
