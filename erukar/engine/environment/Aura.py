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
        self.location = (0,0)
        self.aura_strength = strength
        self.decay_factor = decay_factor

    def affects_tile(self, coordinate):
        pass

    def affects_tile_raw(self, coordinate):
        '''This is used for the quick calculations for the dungeon'''
        dist = math.ceil(self.distance(coordinate))
        strength_at_tile = self.aura_strength * math.pow(self.decay_factor, dist)
        return strength_at_tile >= 1

    def distance(self, to_coordinate):
        return math.sqrt(math.pow(to_coordinate[0]-self.location[0], 2) + math.pow(to_coordinate[1]-self.location[1], 2))
