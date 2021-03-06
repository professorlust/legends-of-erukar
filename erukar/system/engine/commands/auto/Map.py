from erukar.system.engine import Tile, Item, TargetedAbility, Npc
from erukar.system.engine.environment import Door, TransitionPiece
from ..Command import Command


class Map(Command):
    NeedsArgs = False

    '''
    Uses:
        overlay_type
    '''

    def perform(self, *_):
        '''Converts the dungeon_map into a readable map for the user'''
        if 'overlay_type' not in self.args:
            self.args['overlay_type'] = 'visual'
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
            'rooms': {},
            'actions': {},
            'actors': {},
            'lighting': {},
            'coordinates': [],
        }

        if not self.world:
            self.append_result(self.player_info.uid, results)
            return

        self.args['player_lifeform'].build_zones(self.world)
        self.open_space = self.player_zones().all_seen

        # Now get the min and max range for x and y
        max_x, max_y = map(max, zip(*self.open_space))
        min_x, min_y = map(min, zip(*self.open_space))
        results['minX'] = min_x-1
        results['minY'] = min_y-1
        results['width'] = 3 + max_x - min_x
        results['height'] = 3 + max_y - min_y

        for y in range(min_y-1, max_y+2):
            for x in range(min_x-1, max_x+2):
                coord = '({}, {})'.format(x, y)
                results['rooms'][coord] = self.get_room_details(x, y)
                results['actions'][coord] = self.actions_for(x, y)
                results['actors'][coord] = list(self.get_actors_at(x, y))
                results['lighting'][coord] = self.get_lighting_at(x, y)
                results['coordinates'].append(coord)
        self.append_result(self.player_info.uid, results)

    def player_zones(self):
        return self.args['player_lifeform'].zones

    def get_room_details(self, x, y):
        return {
            'title': self.get_title_for(x, y),
            'tile': self.get_tile_at(x, y),
            'walls': self.wall_overlays_at(x, y),
        }

    def get_title_for(self, x, y):
        if (x, y) not in self.player_zones().fog_of_war:
            return 'Unknown: obscured by fog of war'
        aliases = ', '.join(self.alias_actors_at(x, y))
        if aliases:
            return aliases
        return self.world.get_tile_name((x, y)).capitalize()

    def alias_actors_at(self, x, y):
        caller = self.args['player_lifeform']
        for actor in self.world.actors_at(caller, (x, y)):
            if actor in caller.detected_entities:
                yield actor.alias()

    def get_lighting_at(self, x, y):
        if (x, y) in self.player_zones().fog_of_war:
            return Tile.rgba(0, 0, 0, self.world.lighting_at((x, y)))
        return Tile.rgba(0, 0, 0, 0.2)

    def wall_overlays_at(self, x, y):
        return self.world.get_wall_overlay((x, y))

    def get_tile_at(self, x, y):
        if (x, y) not in self.open_space:
            return 'null'
        return self.world.get_tile_at((x, y))

    def get_actors_at(self, x, y):
        caller = self.args['player_lifeform']
        if (x, y) not in caller.zones.fog_of_war:
            return
        for actor in self.world.actors_at(None, (x, y)):
            if actor in caller.detected_entities:
                yield actor.tile_id()

    def action(cmd, desc="", cost=1, target='', weapon='', interaction=''):
        return {
            'command': cmd,
            'cost': cost,
            'description': cmd if not desc else desc,
            'interaction_target': target,
            'weapon': weapon,
            'interaction_type': interaction
        }

    def interact_actions(npc):
        for template in npc.templates:
            if template.is_interactive:
                yield Map.action(
                    cmd='Interact',
                    target=str(npc.uuid),
                    desc=template.interaction_text())

    def transition_action(transition):
        return Map.action(
            cmd='Transition',
            desc='Travel to {}'.format(transition.destination),
            target=str(transition.uuid))

    def basic_action(target):
        interaction_type = 'close' if target.is_open else 'open'
        return Map.action(
            cmd='BasicInteraction',
            desc='{} the door'.format(interaction_type.capitalize()),
            target=str(target.uuid),
            interaction=interaction_type)

    def take_action(item):
        return Map.action(
            cmd='Take',
            desc='Take {}'.format(item.alias()),
            target=str(item.uuid))

    def actions_for(self, x, y):
        actions = []
        player = self.args['player_lifeform']
        loc = (x, y)
        if loc not in player.zones.fog_of_war:
            return []
        if player.action_points() >= 2:
            actions.append(Map.action('Inspect', cost=2))
        actions.append(Map.action('Glance'))

        for door in self.world.actors_of_type_at(player, loc, Door):
            for action in door.actions(player):
                actions.append(action)
        for x in self.world.actors_of_type_at(player, loc, TransitionPiece):
            actions.append(Map.transition_action(x))
        for item in self.world.actors_of_type_at(player, loc, Item):
            actions.append(Map.take_action(item))
        for creature in self.world.creatures_at(player, loc):
            actions += list(Map.append_creature_actions(player, creature, loc))

        # Now go through TargetedAbilities and find relevant ones
        actions += list(self.append_targeted_abilities(loc))
        return actions

    def append_targeted_abilities(self, loc):
        player = self.args['player_lifeform']
        for skill in player.skills:
            if not isinstance(skill, TargetedAbility):
                continue
            if skill.valid_at(self, loc):
                yield from skill.action_for_map(self, loc)

    def append_creature_actions(player, creature, loc):
        if creature and loc in player.zones.fog_of_war:
            if isinstance(creature, Npc):
                yield from Map.interact_actions(creature)
                return

    def overlay_for(self, x, y):
        overlay_method = "get_{}_overlay_for".format(self.args['overlay_type'])
        if hasattr(self, overlay_method):
            overlay = getattr(self, overlay_method)(x, y)
            if overlay:
                return overlay
        return Tile.rgba(0, 0, 0, 0.5)

    def get_movement_overlay_for(self, x, y):
        if any((x, y) == coord for coord in self.player_zones().movement[1]):
            return Tile.rgba(0, 100, 0, 0.2)

        if any((x, y) == coord for coord in self.player_zones().movement[2]):
            return Tile.rgba(0, 80, 80, 0.2)

    def get_visual_overlay_for(self, x, y):
        if any((x, y) == coord for coord in self.player_zones().fog_of_war):
            return Tile.rgba(0, 0, 0, 0)
