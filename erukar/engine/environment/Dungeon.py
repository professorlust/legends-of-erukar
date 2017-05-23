import erukar
from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.calculators.Navigator import Navigator

class Dungeon(RpgEntity):
    minimum_rooms = 3

    def __init__(self):
        super().__init__()
        self.name = "Dungeon"
        self.description = ""
        self.region = ''
        self.sovereignty = ''
        self.dungeon_map = {}
        self.rooms = []
        self.active_auras = set()
        self.actors = set()

    def get_object_by_uuid(self, uuid):
        if uuid == self.uuid: return self

        matched = next((x for x in self.actors if x.uuid == uuid), None)
        if matched: return matched

        for lifeform in (x for x in self.actors if isinstance(x, erukar.engine.lifeforms.Lifeform)):
            matched = lifeform.get_object_by_uuid(uuid)
            if matched: return matched

        for room in self.rooms:
            matched = next((room.get_object_by_uuid(uuid)), None)
            if matched: return matched

    def get_applicable_auras(self, for_loc):
        '''Generator which gets all applicable, active auras at a location'''
        if not isinstance(for_loc, tuple):
            for_loc = for_loc.coordinates
        room_at = self.get_room_at(for_loc)
        if room_at is None:
            return
        for aura in self.active_auras:
            if aura.affects_tile(room_at):
                yield aura

    def add_room(self, new_room, coordinates):
        '''Adds a safeguard to prevent duplication'''
        self.rooms.append(new_room)
        for coord in coordinates:
            self.dungeon_map[coord] = new_room

    def get_room_at(self, location):
        if location in self.dungeon_map:
            return self.dungeon_map[location]
        return None

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

    def add_actor(self, actor, coordinates):
        self.actors.add(actor)
        actor.coordinates = coordinates

    def remove_actor(self, actor):
        self.actors.remove(actor)

    def actors_in_range(self, start, distance):
        for actor in self.actors:
            if Navigator.distance(start, actor.coordinates) <= distance:
                yield actor

    def moving_parts_at(self, coordinates):
        for actor in self.actors:
            if actor.coordinates != coordinates: continue
            if issubclass(type(actor), erukar.engine.inventory.Item):
                return 'item'
            if issubclass(type(actor), erukar.engine.lifeforms.Player):
                return 'player'
            if issubclass(type(actor), erukar.engine.lifeforms.Enemy):
                return 'enemy'
        return ''
