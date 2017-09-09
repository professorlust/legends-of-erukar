from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Sector import Sector

class Region(ErukarObject):
    def __init__(self):
        self.name = 'Basic Region'
        self.description = ''
        self.sectors = set()
        self.sector_template = None
        self.sector_limits = []

    def sector_at(self, coords):
        if coords not in self.sector_limits: return None
        new_sector = next((sector for sector in self.sectors if sector.coordinates() == coords), None)
        if not new_sector:
            new_sector = self.new_sector(coords)
            self.sectors.add(new_sector)
        return new_sector

    def new_sector(self, coords):
        s = Sector(self)
        s.environment_profile = self.sector_template.environment_profile
        s.set_coordinates(coords)
        return s

    def alias(self):
        return self.name
