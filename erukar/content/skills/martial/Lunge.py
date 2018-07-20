from erukar.system.engine import Attack, Move
from erukar.ext.math import Navigator


class Lunge(Attack):
    Name = 'Lunge'
    ShowInLists = True
    Description = 'Lunge at {} with {}'
    CurrentLevel = 'Move up to {:0.0f}% of move speed and then attack '\
        'an enemy with an equipped weapon for {:0.0f}% of normal '\
        'attack damage. Cost 1 Action Point.'
    NextLevel = 'Increases percentage of damage to {:0.0f}%.'

    def valid_at(self, cmd, loc):
        lifeform = cmd.args['player_lifeform']
        origin = lifeform.coordinates
        fog = lifeform.zones.fog_of_war
        if loc not in fog:
            return False
        if not Lunge.has_hostile_at(cmd, loc):
            return False
        dist = Navigator.distance(origin, loc)
        return dist <= self.max_range(cmd)

    def has_hostile_at(cmd, loc):
        player = cmd.args['player_lifeform']
        for creature in cmd.world.creatures_at(player, loc):
            if creature.is_hostile_to(player):
                return True
        return False

    def max_range(self, cmd):
        max_range = -1
        lifeform = cmd.args['player_lifeform']
        move_range = lifeform.move_speed() * Lunge.move_mult(self.level)
        for slot in lifeform.weapon_slots():
            weapon = getattr(lifeform, slot)
            if not weapon:
                continue
            attack_range = weapon.attack_range(lifeform) + move_range
            max_range = attack_range if attack_range > max_range else max_range
        return max_range

    def is_in_valid_range(self, player, weapon, target):
        dist = Navigator.distance(player.coordinates, target.coordinates)
        return dist <= self.attack_range(player, weapon)

    def attack_range(self, player, weapon):
        move_range = player.move_speed() * Lunge.move_mult(self.level)
        return weapon.attack_range(player) + move_range

    def perform_attack(self, cmd, player, weapon, target):
        if not super().is_in_valid_range(player, weapon, target):
            path = Move.get_path_to(cmd, target.coordinates)
            attack_range = weapon.attack_range(player)
            path = path[:-attack_range]
            Move.do_move(cmd, path)
        return super().perform_attack(cmd, player, weapon, target)

    def move_mult(level):
        return 0.8

    def weapon_damage_mult(level):
        return 0.8

    def ap_cost(self, *_):
        return 1

    def modify_damage(self, damage):
        mult = Lunge.weapon_damage_mult(self.level)
        damage = [(amt*mult, d_type) for amt, d_type in damage]
        return damage

    def current_level_description(self):
        move_mult = Lunge.move_mult(self.level)
        weapon_mult = Lunge.weapon_damage_mult(self.level)
        return self.CurrentLevel.format(move_mult, weapon_mult)

    def next_level_description(self):
        move_mult = Lunge.move_mult(self.level + 1)
        weapon_mult = Lunge.weapon_damage_mult(self.level + 1)
        return self.NextLevel.format(move_mult, weapon_mult)
