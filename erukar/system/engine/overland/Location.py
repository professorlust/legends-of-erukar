from erukar.system.engine import EnvironmentProfile

class Location:
    def __init__(self, sector=None):
        self.sector = sector
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Location'

    def adjacent_sectors(self):
        return self.sector.adjacent()

    def coordinates(self):
        return self.sector.coordinates()

    def alias(self):
        return '{} -- {}'.format(self.name, self.sector.alias())
