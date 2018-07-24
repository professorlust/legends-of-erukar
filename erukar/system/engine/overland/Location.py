from erukar.system.engine import EnvironmentProfile, DungeonGenerator


class Location:
    def __init__(self, sector):
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
            return 'error'
        x, y = self.coordinates()
        x_f, y_f = direction_to
        if y == y_f:
            return 'western' if x_f < x else 'eastern'
        if x == x_f:
            return 'northeastern' if y_f > y else 'southwestern'
        return 'northwestern' if y_f > y else 'southeastern'
