from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Location import Location
import operator, re

class Sector(ErukarObject):
    def __init__(self, region, economic_seed_fn=None):
        self.coordinates = ""
        self.environment_profile = EnvironmentProfile()
        self.region = region
        self.adjacent_sectors = set()
        self.locations = set()
        self.name = 'Random Sector'
        self.economic_profile = region.economic_profile\
            if not economic_seed_fn\
            else economic_seed_fn(self)

    def alias(self):
        return self.name

    def set_coordinates(self, new_coords):
        self.coordinates = Sector.autocorrect(new_coords)

    def get_coordinates(self):
        return self.coordinates

    def adjacent(self):
        for sector in self.adjacent_sectors:
            yield sector

    def neighbors(self):
        return list(self.adjacent())

    def distance_to(self, sector):
        '''The sum of all coordinates adds up to zero. By taking the absolute
        value and summing them, you get twice the total distance between two coords.'''
        return -1

    def location(self):
        if len(self.locations) > 0:
            return list(self.locations)[0]
        new_loc = Location(self)
        new_loc.name = self.name
        new_loc.environment_profile = self.environment_profile
        self.locations.add(new_loc)
        return new_loc

    def is_overland(coords):
        if coords is not str: coords = str(coords).replace(' ','')
        return re.match(r'\(([-+]*\d+),([-+]*\d+),([-+]*\d+)\)', coords) is not None

    def autocorrect(coord_string):
        if Sector.is_overland(coord_string):
            return Sector.to_overland(coord_string)
        return coord_string

    def to_overland(coords):
        out = coords
        if isinstance(coords,str):
            out = coords\
                .strip()\
                .replace(' ','')\
                .replace('(','')\
                .replace(')','')\
                .split(',')
        elif not isinstance(coords, tuple) and not isinstance(coords, list):
            raise ValueError('Malformed Overland Coordinates: Unable to parse a non-str non-list non-tuple input (received {})'.format(type(coords)))

        if len(out) != 3:
            raise ValueError('Malformed Overland Coordinates String: Received "{}", which returned "{}"'.format(coords, out))

        return tuple(int(x) for x in out)

    def supply_and_demand_scalar(self, good):
        return self.economic_profile.supply_and_demand_scalar(good)

    def register_transaction(self, good, at_price, supply_shift):
        self.economic_profile.register_transaction(good, at_price, supply_shift)
