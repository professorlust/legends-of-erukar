from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Location import Location

class Sector(ErukarObject):
    def __init__(self, region=None):
        self.set_coordinates((0,0,0))
        self.environment_profile = EnvironmentProfile()
        self.region = region
        self.locations = set()
        self.name = 'Random Sector'

    def alias(self):
        return '{} ({})'.format(self.name, self.coordinates())

    def coordinates(self):
        return (self.x, self.alpha, self.beta)

    def set_coordinates(self, coordinates):
        self.x, self.alpha, self.beta = coordinates

    def adjacent(self):
        sectors = self.region.sector_limits
        if len(sectors) < 2: return
        for neighbor in self.neighbors():
            if neighbor in sectors:
                yield neighbor

    def neighbors(self):
        return [
            (self.x, self.alpha+1, self.beta-1),
            (self.x, self.alpha-1, self.beta+1),
            (self.x+1, self.alpha, self.beta-1),
            (self.x-1, self.alpha, self.beta+1),
            (self.x+1, self.alpha-1, self.beta),
            (self.x-1, self.alpha+1, self.beta),
        ]

    def distance_to(self, sector):
        return all(dist <= 1 for dist in [
            abs(self.x - sector[0]),
            abs(self.alpha - sector[1]),
            abs(self.beta - sector[2])])

    def location(self):
        if len(self.locations) > 1:
            return list(self.locations)[0]
        new_loc = Location(self)
        new_loc.name = self.name
        new_loc.environment_profile = self.environment_profile
        self.locations.add(new_loc)
        return new_loc
