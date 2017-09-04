from erukar.system.engine import EnvironmentProfile, ErukarObject
from .Sector import Sector

class Region(ErukarObject):
    def __init__(self):
        self.name = 'Basic Region'
        self.sectors = [Sector()]

'''
Uses a hexagonal grid to track a user's progression in the region

A region has N sectors, each of which is represented by a dungeon. In some cases, a
sector may have multiple dungeons (multilevel or intra-city).
'''
