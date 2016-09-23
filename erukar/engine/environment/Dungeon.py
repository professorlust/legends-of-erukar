from erukar.engine.model.RpgEntity import RpgEntity

class Dungeon(RpgEntity):
    minimum_rooms = 3

    def __init__(self):
        self.dungeon_map = {}
        self.rooms = []
        self.active_auras = set()

    def get_applicable_auras(self, for_loc):
        '''Generator which gets all applicable, active auras at a location'''
        if not isinstance(for_loc, tuple):
            for_loc = for_loc.coordinates
        room_at = self.get_room_at(for_loc)
        if room_at is None:
            print('room is none')
            return
        for aura in self.active_auras:
            if aura.affects_tile(room_at):
                yield aura

    def get_room_at(self, location):
        return next((x for x in self.rooms if x.coordinates == location), None)

    def auras_for_locations(self, locations):
        '''
        Takes a set of locations (coordinates) and returns a dict of coordinates
        as keys which map to sets of auras that are applicable at that given
        coordinate.
        '''
        return {loc: set(self.get_applicable_auras(loc)) for loc in locations}

    def tick(self):
        self.clean_up_auras()

    def clean_up_auras(self):
        self.active_auras = set(x for x in self.active_auras if not x.is_expired)
