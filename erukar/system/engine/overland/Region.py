from erukar.system.engine import EnvironmentProfile, ErukarObject

class Region(ErukarObject):
    def __init__(self):
        self.name = 'Basic Region'
        self.description = ''
        self.sectors = []
        self.sector_template = None
        self.sector_limits = []

    def sector_at(self, x, alpha, beta):
        if (x,alpha,beta) not in self.sector_limits: return None
        return next((sector for sector in self.sectors if sector.location() == (x, alpha, beta)), self.new_sector(x, alpha, beta))

    def new_sector(self, x, alpha, beta):
        return 'New Sector at {}/{}/{}'.format(x, alpha, beta)
