from erukar.engine.model.RpgEntity import RpgEntity

class Dungeon(RpgEntity):
    minimum_rooms = 3

    def __init__(self):
        self.dungeon_map = {}
        self.rooms = []
        self.active_auras = set()

    def get_applicable_auras(self, for_loc):
        '''Generator which gets all applicable, active auras at a location'''
        for aura in self.active_auras:
            if aura.affects_tile(for_loc):
                yield aura

    def auras_for_locations(self, locations):
        '''
        Takes a set of locations (coordinates) and returns a dict of coordinates
        as keys which map to sets of auras that are applicable at that given
        coordinate.
        '''
        return {loc: set(self.get_applicable_auras(loc)) for loc in locations}

    def clean_up_auras(self):
        self.active_auras = set(x for x in self.active_auras if not x.is_expired)
