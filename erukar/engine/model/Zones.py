from erukar.engine.calculators.Distance import Distance
from erukar.engine.calculators.Navigator import Navigator
import erukar, math

import logging, time
logger = logging.getLogger('debug')

class Zones:
    def __init__(self):
        self.desynced = True
        self.clear()

    def clear(self):
        self.movement = {}
        self.fog_of_war = []
        self.weapon_ranges = {}

    def rebuild_if_desynced(self, lifeform, world):
        if self.desynced:
            self.clear_and_rebuild(lifeform, world.all_traversable_coordinates())

    def clear_and_rebuild(self, lifeform, available_space):
        self.desynced = False
        start_time = time.time()
        self.clear()
        self.build(lifeform, available_space)
        logger.info('Zones -- Clear and rebuild for {} took {:.3f} s to execute'.format(lifeform.name, time.time() - start_time))

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
        self.movement[cost] = Distance.pathed_traversable(start, available_space, (lifeform.move_speed()*cost)-1)

    def compute_fog_of_war(self, lifeform, available_space):
        self.fog_of_war = list(Distance.direct_los(lifeform.coordinates, available_space, lifeform.visual_fog_of_war()))

    def add_all_weapons(self, lifeform):
        for weapon_slot in lifeform.weapon_slots():
            self.compute_weapon_range(lifeform, weapon_slot)

    def compute_weapon_range(self, lifeform, weapon_slot):
        weapon = getattr(lifeform, weapon_slot, None)
        if not weapon or not isinstance(weapon, erukar.engine.inventory.Weapon): return
        for coordinate in self.fog_of_war:
            if Navigator.distance(coordinate, lifeform.coordinates) > weapon.attack_range(lifeform):
                continue
            if coordinate not in self.weapon_ranges:
                self.weapon_ranges[coordinate] = []
            if weapon not in self.weapon_ranges[coordinate]:
                self.weapon_ranges[coordinate].append(weapon)
