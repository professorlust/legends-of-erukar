from erukar.system.engine import ErukarActor, Lifeform
from .Door import Door
from .Wall import Wall
from .Room import Room
from erukar.ext.math import Navigator, Distance

import random
import logging
logger = logging.getLogger('debug')


class Dungeon(ErukarActor):
    GAA_Expects_Coord = 'get_applicable_auras expects a coordinate argument'
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
        self.spawn_coordinates = []
        self.walls = {}
        self.location_transition_coordinates = {}
        self.base_ambient_light = 0
        self.base_ambient_sanctity = 0

        # from 0 to 99.99, where 0 is midnight and 50.0 is midday
        self.time_of_day = 50.0

        # Tiles
        self.tile_set_version = 0
        self.tiles = {}
        self.tile_set = {}
        self.pixel_density = 3
        self.pixels_per_side = 32
        self.tile_generator = None

    def on_start(self):
        super().on_start()
        for room in self.rooms:
            room.on_start()
        for actor in self.actors:
            actor.on_start(self)

    def add_tile(self, tile_id, tile):
        if tile_id in self.tile_set:
            return
        self.tile_set[tile_id] = self.tile_generator.build(tile, tile_id)
        self.tile_set_version += 1

    def add_actor_tiles(self, actor):
        for tile_id in actor.ids_to_generate():
            new_actor = self.tile_generator.build_actor(actor, tile_id)
            self.tile_set[tile_id] = new_actor
            self.tile_set_version += 1

    def refresh_tiles(self):
        self.generate_tiles
        self.tile_set_version += 1

    def generate_tiles(self, tg=None):
        self.tile_generator = tg or self.tile_generator
        for tile in self.tiles.values():
            for tile_id in tile.ids_to_generate():
                if tile_id in self.tile_set:
                    continue
                self.tile_set[tile_id] = tg.build(tile, tile_id)
        for actor in self.actors:
            self.add_actor_tiles(actor)
        self.tile_set_version = 1 if tg else self.tile_set_version + 1

    def get_object_by_uuid(self, uuid):
        if uuid == self.uuid:
            return self
        matched = next((x for x in self.actors if x.uuid == uuid), None)
        if matched:
            return matched
        for lifeform in (x for x in self.actors if isinstance(x, Lifeform)):
            matched = lifeform.get_object_by_uuid(uuid)
            if matched:
                return matched
        for room in self.rooms:
            matched = next((room.get_object_by_uuid(uuid)), None)
            if matched:
                return matched

    def ambient_light(self):
        return self.base_ambient_light

    def lighting_at(self, loc):
        light_sum = self.ambient_light()
        for aura in self.get_applicable_auras(loc):
            if hasattr(aura, 'modify_light'):
                light_sum += aura.modify_light(loc)
        total_light = 0.2 + 0.8 * max(0.0, light_sum)
        return max(0.0, min(1.0, total_light))

    def ambient_sanctity(self):
        return self.base_ambient_sanctity

    def sanctity_at(self, loc):
        aura_sum = self.ambient_sanctity()
        for aura in self.get_applicable_auras(loc):
            if hasattr(aura, 'modify_sanctity'):
                aura_sum += aura.modify_sanctity(loc)
        total_sanctity = min(1, max(-1, aura_sum))
        return total_sanctity

    def get_applicable_auras(self, for_loc):
        '''Generator which gets all applicable, active auras at a location'''
        if not isinstance(for_loc, tuple):
            raise Exception(self.GAA_Expects_Coord)
        for aura in self.active_auras:
            if aura.affects_tile(for_loc):
                yield aura

    def get_tile_at(self, loc):
        if loc in self.tiles:
            return self.tiles[loc].tile_id()
        return 'null'

    def get_tile_name(self, loc):
        if loc in self.tiles:
            return self.tiles[loc].alias()
        return 'Unknown'

    def get_wall_overlay(self, loc):
        overlays = []
        if loc not in self.dungeon_map:
            return overlays
        # Check to the Left
        if (loc[0]-1, loc[1]) in self.walls:
            overlays.append('wall left')
        # Check to the Right
        if (loc[0]+1, loc[1]) in self.walls:
            overlays.append('wall right')
        # Check Above
        if (loc[0], loc[1]-1) in self.walls:
            overlays.append('wall top')
        # Check Below
        if (loc[0], loc[1]+1) in self.walls:
            overlays.append('wall bottom')
        return overlays

    def add_room(self, new_room, coordinates):
        '''Adds a safeguard to prevent duplication'''
        self.rooms.append(new_room)
        self.annex(new_room, coordinates)

    def annex(self, room, coordinates):
        for coord in coordinates:
            self.dungeon_map[coord] = room

    def actors_at(self, caller, coordinate):
        for x in self.actors:
            if x is not caller and x.coordinates == coordinate:
                yield x

    def creatures_at(self, caller, coordinate):
        yield from self.actors_of_type_at(caller, coordinate, Lifeform)

    def actors_of_type_at(self, caller, coordinate, actor_type):
        for x in self.actors_at(caller, coordinate):
            if isinstance(x, actor_type):
                yield x

    def all_traversable_coordinates(self):
        '''Move to player later'''
        return list(self.traversable_coordinates_generator())

    def traversable_coordinates_generator(self):
        if not hasattr(self, 'door_cache'):
            self.build_door_cache()
        for loc in self.dungeon_map:
            if loc in self.door_cache:
                if any(not x.is_open for x in self.door_cache[loc]):
                    continue
            yield loc

    def is_traversable(self, loc):
        return loc in self.dungeon_map \
            and all(x.is_open for x in self.door_cache.get(loc, []))

    def build_door_cache(self):
        self.door_cache = {}
        for loc in self.dungeon_map:
            doors = list(self.actors_of_type_at(None, loc, Door))
            if any(doors):
                self.door_cache[loc] = doors

    def get_room_at(self, location):
        if location in self.dungeon_map:
            return self.dungeon_map[location]
        return None

    def apply_tiles_on_all_closed_space(self, tile):
        xo, yo = map(min, zip(*self.dungeon_map))
        xf, yf = map(max, zip(*self.dungeon_map))
        for y in range(yo-1, yf+2):
            for x in range(xo-1, xf+2):
                if (x, y) not in self.dungeon_map:
                    if (x, y) not in self.walls:
                        wall = Wall()
                        wall.material = tile
                        self.walls[(x, y)] = wall
                    self.tiles[(x, y)] = tile

    def apply_tiles_on_closed_space(self, spaces, tile):
        for space in spaces:
            if space in self.dungeon_map:
                continue
            self.tiles[space] = tile

    def apply_tiles_on_all_open_space(self, tile):
        for space in self.dungeon_map:
            self.tiles[space] = tile

    def apply_tiles_on_open_space(self, spaces, tile):
        for space in spaces:
            if space not in self.dungeon_map:
                continue
            self.tiles[space] = tile

    def apply_tiles_to_room(self, room, open_tile=None, closed_tile=None):
        if open_tile:
            self.apply_tiles_on_open_space(room.coordinates, open_tile)

    def deintersect(self, space):
        for loc in space:
            if self.is_traversable(loc):
                yield loc

    def remove_space(self, closed_space):
        for space in closed_space:
            if space in self.dungeon_map:
                self.dungeon_map.pop(space, None)

    def initiate_aura(self, aura, location):
        aura.location = location
        self.active_auras.add(aura)

    def auras_for_locations(self, locations):
        '''
        Takes a set of locations (coordinates) and returns a dict of
        coordinates as keys which map to sets of auras that are
        applicable at that given coordinate.
        '''
        return {loc: set(self.get_applicable_auras(loc)) for loc in locations}

    def tick(self, cmd):
        self.time_of_day = (self.time_of_day + 0.75) % 100.0
        self.clean_up_auras()

    def clean_up_auras(self):
        self.active_auras = set(self.not_expired_auras())

    def not_expired_auras(self):
        for x in self.active_auras:
            if not x.is_expired:
                yield x

    def add_door(self, door, coordinates):
        self.add_actor(door, coordinates)
        self.build_door_cache()

    def add_transition(self, trans, coordinates):
        self.add_actor(trans, coordinates)
        self.location_transition_coordinates[trans.destination] = coordinates

    def add_actor(self, actor, loc):
        self.actors.add(actor)
        if isinstance(loc, Room):
            loc = random.choice(loc.coordinates)
        actor.world = self
        actor.coordinates = loc
        if self.tile_generator:
            self.add_actor_tiles(actor)

    def add_npc(self, npc, coordinates):
        for template in npc.inactive_templates:
            template(self).apply(npc)
        npc.inactive_templates = []
        self.add_actor(npc, coordinates)

    def remove_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def actors_in_range(self, start, distance):
        for actor in self.actors:
            if Navigator.distance(start, actor.coordinates) <= distance:
                yield actor

    def actors_in_range_los(self, caller, start, distance):
        coords = list(Distance.direct_los(
            origin=start,
            open_space=self.all_traversable_coordinates(),
            max_distance=distance
        ))
        for coord in coords:
            yield from self.actors_at(caller, coord)

    def sentient_actors(self, caller):
        for actor in self.actors:
            if actor is caller:
                continue
            if isinstance(actor, Lifeform):
                yield actor

    def moving_parts_at(self, coordinates):
        for actor in self.actors:
            if actor.coordinates != coordinates:
                continue
            return str(actor.uuid)
        return ''

    def economy(self):
        return self.location.economic_profile
