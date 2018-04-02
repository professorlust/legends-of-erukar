from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Sector import Sector
from .Location import Location
import operator

class OverlandSector(Sector):
    def __init__(self, region=None):
        super().__init__(region)
        self.coordinates = "(0,0,0)"
        self.x = 0
        self.alpha = 0
        self.beta = 0

    def alias(self):
        return '{} {}'.format(self.name, self.get_coordinates())

    def adjacent(self):
        sectors = self.region.sector_limits
        if len(sectors) < 2: return
        for neighbor in self.neighbors():
            if neighbor in sectors:
                yield neighbor

    def get_coordinates(self):
        return (self.x, self.alpha, self.beta)

    def to_coords(x,alpha,beta):
        return '({},{},{})'.format(x,alpha,beta)

    def set_coordinates(self, coords):
        out = Sector.to_overland(coords)
        self.x,self.alpha,self.beta = [int(x) for x in out]

    def neighbors(self):
        return [
            (self.x,   self.alpha+1, self.beta-1),
            (self.x,   self.alpha-1, self.beta+1),
            (self.x+1, self.alpha,   self.beta-1),
            (self.x-1, self.alpha,   self.beta+1),
            (self.x+1, self.alpha-1, self.beta),
            (self.x-1, self.alpha+1, self.beta),
        ]

    def distance_to(self, sector):
        '''The sum of all coordinates adds up to zero. By taking the absolute
        value and summing them, you get twice the total distance between two coords.'''
        return int(sum([abs(x) for x in tuple(map(operator.sub, self.coordinates(), sector))])/2)
