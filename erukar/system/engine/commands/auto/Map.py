from erukar.system.engine import Tile, Item
from erukar.system.engine.environment import *
from erukar.ext.math import Distance
from ..Command import Command
import math
import logging

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
            'pixel': {
                'density': self.world.pixel_density,
                'numberOnASide': self.world.pixels_per_side
            },
            'rooms': []
        }

        if not self.world:
            self.append_result(self.player_info.uid, results)
            return

        self.args['player_lifeform'].build_zones(self.world)
        self.open_space = self.args['player_lifeform'].zones.all_seen

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
            'coordinates': [x, y],
            'tile': self.layers_for(x,y),
            'walls': self.wall_overlays_at(x, y),
            'actors': list(self.get_actors_at(x,y)),
            'actions': self.actions_for(x, y)
        }

    def wall_overlays_at(self, x, y):
        return self.world.get_wall_overlay((x,y))

    def layers_for(self, x, y):
        if (x,y) not in self.open_space:
            return 'null'
        if (x,y) in self.world.all_traversable_coordinates():
            return self.world.get_floor_type((x,y))
        return self.world.get_wall_type((x,y))

    def get_actors_at(self, x, y):
        for actor in self.world.actors_at(self.args['player_lifeform'], (x,y)):
            yield str(actor.uuid)

    def action(command, description="", cost=1, target='', weapon=''):
        return {
            'command': command,
            'cost': cost,
            'description': command if not description else description,
            'interaction_target': target,
            'weapon': weapon
        }

    def attack_action(weapon, creature):
        return Map.action('Attack', description='Attack with {}'.format(weapon.alias()), weapon=str(weapon.uuid), target=str(creature.uuid))

    def interact_actions(npc):
        for template in npc.templates:
            if template.is_interactive:
                yield Map.action('Interact', target=str(npc.uuid), description=template.interaction_text(npc))

    def transition_action(transition):
        return Map.action('Transition', description='Travel to {}'.format(transition.destination), target=str(transition.uuid))

    def take_action(item):
        return Map.action('Take', description='Take {}'.format(item.alias()), target=str(item.uuid))

    def actions_for(self, x, y):
        actions = []
        player = self.args['player_lifeform']
        loc = (x,y)

        if player.action_points() >= 2:
            actions.append(Map.action('Inspect', cost=2))
        actions.append(Map.action('Glance'))

        move = self.move_action(x,y)
        if move: actions.append(move)

        for transition in self.world.actors_of_type_at(player, loc, TransitionPiece):
            actions.append(Map.transition_action(transition))
        for item in self.world.actors_of_type_at(player, loc, Item):
            actions.append(Map.take_action(item))
        for creature in self.world.creatures_at(player, loc):
            actions += list(Map.append_creature_actions(player, creature, loc))
        return actions

    def append_creature_actions(player, creature, loc):
        if creature and loc in player.zones.fog_of_war:
            if not creature.is_hostile_to(player):
                yield from Map.interact_actions(creature)
                return
            for weapon in player.zones.weapon_ranges.get(loc, []):
                yield Map.attack_action(weapon, creature)

    def move_action(self, x,y):
        move_sets = self.args['player_lifeform'].zones.movement
        applicable_move_costs = [cost for cost in move_sets if (x,y) in move_sets[cost]]
        if not applicable_move_costs: return None

        return Map.action('Move', cost=min(applicable_move_costs))

    def overlay_for(self, x,y):
        overlay_method_name = "get_{}_overlay_for".format(self.args['overlay_type'])
        if hasattr(self, overlay_method_name):
            overlay = getattr(self, overlay_method_name)(x, y)
            if overlay: return overlay

        return Tile.rgba(0, 0, 0, 0.5)

    def get_movement_overlay_for(self, x,y):
        if any((x,y) == coord for coord in self.args['player_lifeform'].zones.movement[1]):
            return Tile.rgba(0, 100, 0, 0.2)

        if any((x,y) == coord for coord in self.args['player_lifeform'].zones.movement[2]):
            return Tile.rgba(0, 80, 80, 0.2)

    def get_visual_overlay_for(self, x,y):
        if any((x,y) == coord for coord in self.args['player_lifeform'].zones.fog_of_war):
            return Tile.rgba(0, 0, 0, 0)
