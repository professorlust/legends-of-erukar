from erukar.system.engine import EnvironmentProfile, DungeonGenerator

class Location:
    def __init__(self, sector=None):
        self.sector = sector
        self.chunks = [] # See config/world/chunks/
        self.environment_profile = EnvironmentProfile() if not sector else sector.environment_profile
        self.name = 'Base Location'
        self.is_named = False
        self.dungeon_file_name = None
        self.economic_profile = sector.economic_profile

    def adjacent_sectors(self):
        return self.sector.adjacent()

    def coordinates(self):
        return self.sector.get_coordinates()

    def alias(self):
        if self.is_named:
            return '{} -- {}'.format(self.name, self.sector.alias())
        return '{}, {}'.format(self.sector.alias(), self.sector.region.alias())

    def get_dungeon(self):
        if self.dungeon_file_name:
            dungeon = __import__(self.dungeon_file_name).dungeon
        else: dungeon = self.random_dungeon() 

        dungeon.overland_location = self
        return dungeon

    def random_dungeon(self):
        generator = DungeonGenerator(self)
        return generator.generate()

    def direction_to(self, direction_to):
        here = self.coordinates()
        if isinstance(here, str): return 'central'
        if direction_to[0] == here[0]:
            return 'western' if direction_to[1] > here[1] else 'eastern'
        if direction_to[1] == here[1]:
            return 'southwestern' if direction_to[0] > here[0] else 'northeastern'
        return 'southeastern' if direction_to[0] > here[0] else 'northwestern'
