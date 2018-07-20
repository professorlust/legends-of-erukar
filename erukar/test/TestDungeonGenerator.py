from erukar import DungeonGenerator, Location, Sector, Region
from .FrameworkDungeon import FrameworkDungeon


class TestDungeonGenerator(DungeonGenerator):
    def __init__(self, location=None):
        location = location or Location(Sector(Region()))
        super().__init__(location)

    def generate(self):
        return super().generate(FrameworkDungeon)
