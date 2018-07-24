from .Sector import Sector


class OverlandSector(Sector):
    def __init__(self, region=None, econ_seed_fn=None):
        super().__init__(region, econ_seed_fn)
        self.coordinates = "(0,0)"
        self.use_day_night_cycle = True
        self.x = 0
        self.y = 0

    def gamma(self):
        return -(self.x + self.y)

    def alias(self):
        return '{} {}'.format(self.name, self.get_coordinates())

    def adjacent(self):
        sectors = self.region.sector_limits
        if len(sectors) < 2:
            return
        for neighbor in self.neighbors():
            if neighbor in sectors:
                yield neighbor

    def get_coordinates(self):
        return (self.x, self.y)

    def to_coords(x, y):
        return '({},{})'.format(x, y)

    def set_coordinates(self, coords):
        out = Sector.to_overland(coords)
        self.x, self.y = [int(x) for x in out]

    def neighbors(self):
        return [
            (self.x-1, self.y),
            (self.x+1, self.y),
            (self.x, self.y-1),
            (self.x, self.y+1),
            (self.x+1, self.y-1),
            (self.x-1, self.y+1),
        ]

    def distance_to(self, sector):
        return max(
            abs(self.x - sector.x),
            abs(self.y - sector.y),
            abs(self.gamma() - sector.gamma())
        )
