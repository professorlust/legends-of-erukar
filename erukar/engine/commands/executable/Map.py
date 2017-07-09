from erukar.engine.commands.executable.Inspect import Inspect
from erukar.engine.commands.Command import Command
from erukar.engine.environment import *
from erukar.engine.model.CoordinateTranslator import CoordinateTranslator
from erukar.engine.model.Direction import Direction
from erukar.engine.calculators.Distance import Distance
import erukar, math

class Map(Command):
    NeedsArgs = False

    '''
    Uses:
        overlay_type
    '''

    def perform(self, *_):
        '''Converts the dungeon_map into a readable map for the user'''
        if 'overlay_type' not in self.args: self.args['overlay_type'] = 'visual'

        self.dimensional_map()
        return self.succeed()

    def translate_coordinates_to_grid(coords):
        return tuple(map(lambda y: 2*y+1, coords))

    def translate_grid_to_coordinates(grid):
        return tuple(map(lambda y: int((y-1)/2), grid))

    def dimensional_map(self):
        self.open_space = []
#       # Iterate over all of the rooms the player knows about
        results = {
            'minX': 0,
            'minY': 0,
            'height': 1,
            'width': 1,
            'rooms': [] # 
        }

        if not self.world:
            self.append_result(self.player_info.uid, results)
            return

        self.open_space = self.world.all_traversable_coordinates()
        self.prepare_zones()

        # Now get the min and max range for x and y
        max_x, max_y = map(max, zip(*self.open_space))
        min_x, min_y = map(min, zip(*self.open_space))
        results['minX'] = min_x-1
        results['minY'] = min_y-1
        results['width'] = 3 + max_x - min_x
        results['height'] = 3 + max_y - min_y

        for y in range(min_y-1, max_y+2):
            for x in range(min_x-1, max_x+2):
                details = self.get_room_details(x, y)
                results['rooms'].append(details)
        self.append_result(self.player_info.uid, results)

    def get_room_details(self, x, y):
        return {
            'overlay': self.overlay_for(x,y),
            'layers': self.layers_for(x,y),
            'actions': self.actions_for(x, y)
        }

    def layers_for(self, x, y):
        result = ['cement']
        if (x,y) not in self.open_space:
            result.append('wood wall')
        result.append(self.world.moving_parts_at((x,y)))
        return result

    def actions_for(self, x, y):
        actions = {
            'Inspect': {'cost': 2},
            'Glance': {'cost': 1},
        }
        if (x,y) in self.one_ap_movement:
            actions['Move'] = {'cost': 1}
        elif (x,y) in self.two_ap_movement:
            actions['Move'] = {'cost': 2}

        creature_at = self.world.creature_at(self.args['player_lifeform'], (x,y))
        if creature_at and (x,y) in self.visual_fog_of_war and (x,y) in self.weapon_attack_ranges:
            for weapon in self.weapon_attack_ranges[(x,y)]:
                actions['Attack with {}'.format(weapon.describe())] = {
                    'method': 'Attack',
                    'cost': 1,
                    'weapon': str(weapon.uuid),
                    'interaction_target': str(creature_at.uuid)
                }

        return actions

    def prepare_zones(self):
        start = self.args['player_lifeform'].coordinates 
        move_speed = self.args['player_lifeform'].move_speed()
        v_fow = self.args['player_lifeform'].visual_fog_of_war()

        self.two_ap_movement = Distance.pathed_traversable(start, self.open_space, (move_speed*2)-1)
        self.one_ap_movement = Distance.pathed_traversable(start, self.two_ap_movement, move_speed-1)
        self.visual_fog_of_war = list(Distance.direct_los(start, self.open_space, v_fow))

        self.weapon_attack_ranges = {}
        for weapon_slot in self.args['player_lifeform'].weapon_slots():
            self.add_weapon_range(weapon_slot, start)

    def add_weapon_range(self, weapon_slot, start):
        weapon = getattr(self.args['player_lifeform'], weapon_slot)
        if not isinstance(weapon, erukar.engine.inventory.Weapon): return
        for coord in Distance.direct_los(start, self.open_space, weapon.MaximumRange):
            if coord not in self.weapon_attack_ranges:
                self.weapon_attack_ranges[coord] = []
            self.weapon_attack_ranges[coord].append(weapon)

    def overlay_for(self, x,y):
        overlay_method_name = "get_{}_overlay_for".format(self.args['overlay_type'])
        if hasattr(self, overlay_method_name):
            overlay = getattr(self, overlay_method_name)(x, y)
            if overlay: return overlay

        return Map.rgba(0, 0, 0, 0.5)

    def get_movement_overlay_for(self, x,y):
        if any((x,y) == coord for coord in self.one_ap_movement):
            return Map.rgba(0, 100, 0, 0.3)

        if any((x,y) == coord for coord in self.two_ap_movement):
            return Map.rgba(0, 80, 80, 0.2)

    def get_visual_overlay_for(self, x,y):
        if any((x,y) == coord for coord in self.visual_fog_of_war):
            return Map.rgba(0, 0, 0, 0)

    def rgba(r,g,b,a):
        return { 'r': r, 'g': g, 'b': b, 'a': a }

