import erukar, random
from erukar.ext.math import Pathing

import logging, time
logger = logging.getLogger('debug')

class BaseAI:
    MaxCalls = 5

    def create_command(caller, world, cmd_type):
        cmd = cmd_type()
        cmd.world = world
        cmd.player_info = caller
        cmd.args = {}
        return cmd

    def perform_turn(caller, instance):
        for _ in range(BaseAI.MaxCalls):
            new_command = BaseAI.get_desired_command(caller, instance)
            instance.try_execute(caller, new_command)
            if isinstance(new_command, erukar.system.engine.commands.executable.Wait) or caller.action_points() <= 0:
                break
        if caller.action_points() > 0:
            wait = BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Wait)
            instance.try_execute(caller, wait)

    def get_desired_command(caller, instance):
        target, weapons = BaseAI.check_for_enemies_in_range(caller, instance.dungeon)
        if target:
            weapon = caller.right
            if not weapon:
                return BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Wait)
            return BaseAI.create_attack(caller, instance.dungeon, target, weapon)

        location = BaseAI.check_for_enemies_to_move_to(caller, instance.dungeon)
        if location: return BaseAI.create_movement(caller, instance.dungeon, location)

        if caller.action_points() >= 2:
            return BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Wait)
        return BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Inspect)


    def check_for_enemies_in_range(caller, world):
        for loc in caller.zones.weapon_ranges:
            for player in world.actors_of_type_at(caller, loc, erukar.system.engine.Player):
                return player, caller.zones.weapon_ranges[loc]
        return None, []

    def check_for_enemies_to_move_to(caller, world):
        for loc in caller.zones.fog_of_war:
            for player in world.actors_of_type_at(caller, loc, erukar.system.engine.Player):
                return BaseAI.get_nearest_coordinate_in_attack_range(caller, world, loc)
        return None

    def create_attack(caller, world, target, weapon):
        cmd = BaseAI.create_command(caller, world, erukar.engine.commands.executable.Attack)
        cmd.args['interaction_target'] = target.uuid
        cmd.args['weapon'] = weapon.uuid
        return cmd

    def create_movement(caller, world, location):
        cmd = BaseAI.create_command(caller, world, erukar.engine.commands.executable.Move)
        cmd.args['coordinates'] = location
        return cmd

    def get_nearest_coordinate_in_attack_range(caller, world, goal):
        '''Will make more efficient later'''
        path = BaseAI.get_path_to(caller, world, goal)
        max_weapon_range = caller.max_weapon_range()
        travel_distance = caller.move_speed() * caller.action_points()
        if (len(path) - max_weapon_range) <= travel_distance:
            return path[max(0,len(path) - max_weapon_range - 1)]
        return path[travel_distance - 1]

    def get_path_to(caller, world, goal):
        start = caller.coordinates
        collection = world.all_traversable_coordinates()

        pather = Pathing(collection)
        path_info, cost = pather.search(collection, start, goal)
        path = pather.reverse(path_info, start, goal)
        if path: path.pop(0)
        return path
