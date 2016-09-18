from erukar.engine.model.Describable import Describable
import math

class Aura(Describable):
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
        self.is_expired = False

    def affects_tile(self, coordinate):
        '''This is used for the quick calculations for the dungeon'''
        dist = math.ceil(self.distance(coordinate))
        strength_at_tile = self.aura_strength * math.pow(self.decay_factor, dist)
        return strength_at_tile >= 1

    def distance(self, to_coordinate):
        return math.sqrt(sum(math.pow(a-b, 2) for a,b in zip(self.location, to_coordinate)))

    def tick(self):
        '''
        Time-based, regular Tick that occurs every 25 ticks in a TurnManager (5 seconds).
        For time-based auras, this might decrement a timer function. If that timer is at 
        zero at the end, it sets the expired flag to true, then is removed by the dungeon 
        on the next cleanup cycle
        '''
        pass
