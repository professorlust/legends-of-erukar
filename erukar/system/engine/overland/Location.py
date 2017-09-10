from erukar.system.engine import EnvironmentProfile, DungeonGenerator

class Location:
    def __init__(self, sector=None):
        self.sector = sector
        self.environment_profile = EnvironmentProfile()
        self.name = 'Base Location'
        self.is_named = False
        self.dungeon_file_name = None

    def adjacent_sectors(self):
        return self.sector.adjacent()

    def coordinates(self):
        return self.sector.coordinates()

    def alias(self):
        if self.is_named:
            return '{} -- {}'.format(self.name, self.sector.alias())
        return '{}, {}'.format(self.sector.alias(), self.sector.region.alias())

    def get_dungeon(self):
        if self.dungeon_file_name:
            return __import__(self.dungeon_file_name).dungeon
        return self.random_dungeon() 

    def random_dungeon(self):
        generator = DungeonGenerator(self)
        return generator.generate()

