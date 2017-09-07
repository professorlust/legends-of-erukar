class Location:
    def __init__(self, sector=None):
        self.sector = sector
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Sector'
