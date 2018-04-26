from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Sector import Sector
from .OverlandSector import OverlandSector
from .EconomicProfile import EconomicProfile

class Region(ErukarObject):
    def __init__(self, economic_seed_fn=None):
        self.name = 'Basic Region'
        self.description = ''
        self.sectors = {}
        self.sector_template = None
        self.sector_limits = []
        self.default_sector = None
        self.economic_profile = EconomicProfile(economic_seed_fn)

    def add_sector(self, sector_fn):
        new_sector = sector_fn(self)
        if self.default_sector is None:
            self.default_sector = new_sector
        coords = new_sector.get_coordinates()
        self.sectors[coords] = new_sector

    def sector_at(self, coords):
        if coords in self.sectors:
            return self.sectors[coords]

        if coords in self.sector_limits:
            new_sector = self.new_sector(coords)
            self.sectors[new_sector.get_coordinates()] = new_sector
            return new_sector

    def new_sector(self, coords):
        s = OverlandSector(self)
        s.environment_profile = self.sector_template.environment_profile
        s.set_coordinates(coords)
        return s

    def alias(self):
        return self.name
