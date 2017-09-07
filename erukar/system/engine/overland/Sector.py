from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Region import Region

class Sector(ErukarObject):
    def __init__(self, region=None):
        self.set_location(0,0,0)
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Sector'
        self.region = region if region else Region()
        self.locations = []

    def location(self):
        return (self.x, self.alpha, self.beta)

    def set_location(self, x, alpha, beta):
        self.x = x
        self.alpha = alpha
        self.beta = beta
