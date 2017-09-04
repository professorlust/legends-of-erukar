from erukar.system.engine import EnvironmentProfile, ErukarObject

class Sector(ErukarObject):
    def __init__(self):
        self.x = 0
        self.alpha = 0
        self.beta = 0
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Sector'

    def location(self):
        return (self.x, self.alpha, self.beta)
