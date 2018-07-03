from .Dungeon import Dungeon
import math


class OverlandZone(Dungeon):
    def ambient_light(self):
        x = self.time_of_day
        return 0.5 + 0.5*math.sin(math.pi * ((x-25)/50))
