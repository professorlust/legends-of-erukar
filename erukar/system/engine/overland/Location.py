from erukar.system.engine import EnvironmentProfile, DungeonGenerator


class Location:
    def __init__(self, sector=None):
        self.sector = sector
        self.chunks = [] # See config/world/chunks/
        self.environment_profile = getattr(sector, 'environment_profile', EnvironmentProfile())
        self.name = 'Base Location'
        self.is_named = False
        self.use_day_night_cycle = getattr(sector, 'use_day_night_cycle', False)
        self.dungeon_file_name = None
        self.ambient_light = 0
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
        else:
            dungeon = self.random_dungeon()

        dungeon.overland_location = self
        return dungeon

    def random_dungeon(self):
        generator = DungeonGenerator(self)
        return generator.generate()

    def direction_to(self, direction_to):
        if isinstance(self.coordinates(), str):
            return 'central'
        x, y, z = self.coordinates()
        if direction_to[0] == x:
            return 'western' if direction_to[1] > y else 'eastern'
        if direction_to[1] == y:
            return 'southwestern' if direction_to[0] > x else 'northeastern'
        return 'southeastern' if direction_to[0] > x else 'northwestern'
