from .Move import Move
from .Attack import Attack
from ..lifeforms.Enemy import Enemy
from ..environment import Door


class MicroMove(Move):
    def valid_at(self, cmd, loc):
        False

    def perform(self, cmd):
        direction = cmd.args.get('direction')
        if not direction:
            return cmd.fail('No direction specified')
        method = 'move_{}'.format(direction)
        return getattr(self, method)(cmd)

    def move_left(self, cmd):
        current = cmd.args['player_lifeform'].coordinates
        coord = (current[0]-1, current[1])
        return MicroMove.do_move(cmd, coord)

    def move_right(self, cmd):
        current = cmd.args['player_lifeform'].coordinates
        coord = (current[0]+1, current[1])
        return MicroMove.do_move(cmd, coord)

    def move_up(self, cmd):
        current = cmd.args['player_lifeform'].coordinates
        coord = (current[0], current[1]-1)
        return MicroMove.do_move(cmd, coord)

    def move_down(self, cmd):
        current = cmd.args['player_lifeform'].coordinates
        coord = (current[0], current[1]+1)
        return MicroMove.do_move(cmd, coord)

    def do_move(cmd, coord):
        if not cmd.world.is_traversable(coord):
            return cmd.fail('Cannot move in this direction')
        player = cmd.args.get('player_lifeform')
        if MicroMove.should_attack(player, coord, cmd):
            return cmd.perform()
        cmd_res = MicroMove.should_door(player, coord, cmd)
        if cmd_res:
            return cmd_res
        if not player.provision_movement_points():
            return cmd.fail('Cannot move!')
        player.movement_allowed -= 1
        Move.do_move(cmd, [coord])
        return cmd.succeed()

    def should_attack(player, loc, cmd):
        enemy = next(cmd.world.actors_of_type_at(player, loc, Enemy), None)
        if not enemy:
            return False
        weapon = next(Attack.weapons_in_range(player, loc), None)
        if not weapon:
            return False
        cmd.args['interaction_target'] = enemy
        cmd.args['weapon'] = weapon
        cmd.args['abilityModule'] = Attack.__module__
        return True

    def should_door(player, loc, cmd):
        door = next(cmd.world.actors_of_type_at(player, loc, Door), None)
        if not door or door.is_open:
            return None
        if door.lock_type:
            return door.on_unlock(cmd)
        return door.on_open(cmd)
