import erukar, random

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
            new_command = None

            target, weapons = BaseAI.check_for_enemies_in_range(caller, instance.dungeon)
            if target:
                weapon = random.choice(weapons)
                new_command = BaseAI.create_attack(caller, instance.dungeon, target, weapon)

            if not new_command:
                target, location = BaseAI.check_for_enemies_to_move_to(caller, instance.dungeon)
                if target: new_command = BaseAI.create_movement(caller, instance.dungeon, location)

            if not new_command:
                new_command = BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Wait)

            logger.info('BaseAI -- {} is executing a {} ({} AP remaining)'.format(caller, new_command, caller.action_points()))
            instance.try_execute(caller, new_command)
            if isinstance(new_command, erukar.engine.commands.executable.Wait) or caller.action_points() <= 0:
                logger.info('BaseAI -- Exiting')
                break

    def check_for_enemies_in_range(caller, dungeon):
        for loc in caller.zones.weapon_ranges:
            x = dungeon.creature_at(caller, loc)
            if x: return x, caller.zones.weapon_ranges[loc]
        return None, []

    def check_for_enemies_to_move_to(caller, dungeon):
        return None, []

    def create_attack(caller, world, target, weapon):
        cmd = BaseAI.create_command(caller, world, erukar.engine.commands.executable.Attack)
        cmd.args['interaction_target'] = target.uuid
        cmd.args['weapon'] = weapon.uuid
        return cmd

    def create_movement(caller, world, location):
        cmd = BaseAI.create_command(caller, world, erukar.engine.commands.executable.Attack)
        cmd.args['coordinates'] = location
        return cmd
