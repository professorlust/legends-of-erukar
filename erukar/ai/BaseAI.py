import erukar, random

import logging, time
logger = logging.getLogger('debug')

class BaseAI:
    def create_command(caller, world, cmd_type):
        cmd = cmd_type()
        cmd.world = world
        cmd.player_info = caller
        cmd.args = {}
        return cmd

    def perform_turn(caller, instance):
        target, weapons = BaseAI.check_for_enemies_in_range(caller, instance.dungeon)
        new_command = BaseAI.create_command(caller, instance.dungeon, erukar.engine.commands.executable.Wait)
        if target:
            weapon = random.choice(weapons)
            new_command = BaseAI.create_attack(caller, instance.dungeon, target, weapon)
        instance.try_execute(caller, new_command)

    def check_for_enemies_in_range(caller, dungeon):
        for loc in caller.zones.weapon_ranges:
            x = dungeon.creature_at(caller, loc)
            if x: return x, caller.zones.weapon_ranges[loc]
        return None, []

    def create_attack(caller, world, target, weapon):
        cmd = BaseAI.create_command(caller, world, erukar.engine.commands.executable.Attack)
        cmd.args['interaction_target'] = target.uuid
        cmd.args['weapon'] = weapon.uuid
        return cmd
