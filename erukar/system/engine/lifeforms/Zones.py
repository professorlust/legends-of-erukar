from erukar.ext.math import Distance, Navigator
from erukar.system.engine import Weapon
import logging
import time
logger = logging.getLogger('debug')


class Zones:
    BuildLogFmt = 'Zones -- Clear and rebuild for {} took {:.3f} s to execute'

    def __init__(self):
        self.desynced = True
        self.all_seen = set()
        self.clear()

    def clear(self):
        self.movement = {}
        self.fog_of_war = []
        self.weapon_ranges = {}

    def rebuild_if_desynced(self, lifeform, world):
        if self.desynced:
            space = world.all_traversable_coordinates()
            self.clear_and_rebuild(lifeform, space)

    def clear_and_rebuild(self, lifeform, available_space):
        self.desynced = False
        start_time = time.time()
        self.clear()
        self.build(lifeform, available_space)
        d_time = time.time() - start_time
        logger.info(Zones.BuildLogFmt.format(lifeform.name, d_time))

    def build(self, lifeform, available_space):
        self.add_all_movements(lifeform.coordinates, lifeform, available_space)
        self.compute_fog_of_war(lifeform, available_space)
        self.add_all_weapons(lifeform)
        self.desynced = False

    def add_all_movements(self, start, lifeform, available_space):
        previous_set = available_space
        for cost in reversed(range(1, lifeform.action_points()+1)):
            self.add_movement(start, lifeform, previous_set, cost)
            previous_set = self.movement[cost]

    def add_movement(self, start, lifeform, available_space, cost):
        potential_speed = (lifeform.move_speed() * cost) - 1
        self.movement[cost] = Distance.pathed_traversable(
            origin=start,
            traversable_collection=available_space,
            max_tiles=potential_speed)

    def compute_fog_of_war(self, lifeform, available_space):
        coords = lifeform.coordinates
        fog_of_war = lifeform.visual_fog_of_war()
        los = Distance.direct_los(coords, available_space, fog_of_war)
        for seen in los:
            self.fog_of_war.append(seen)
            self.all_seen.add(seen)

    def add_all_weapons(self, lifeform):
        for weapon_slot in lifeform.weapon_slots():
            self.compute_weapon_range(lifeform, weapon_slot)

    def compute_weapon_range(self, lifeform, weapon_slot):
        weapon = getattr(lifeform, weapon_slot, None)
        if not weapon or not isinstance(weapon, Weapon):
            return
        attack_range = weapon.attack_range(lifeform)
        for coord in self.fog_of_war:
            if Navigator.distance(coord, lifeform.coordinates) > attack_range:
                continue
            if coord not in self.weapon_ranges:
                self.weapon_ranges[coord] = []
            if weapon not in self.weapon_ranges[coord]:
                self.weapon_ranges[coord].append(weapon)
