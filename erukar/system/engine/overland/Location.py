from erukar.system.engine import EnvironmentProfile
from .Sector import Sector

class Location:
    def __init__(self, sector=None):
        self.sector = sector if sector else Sector()
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Sector'
