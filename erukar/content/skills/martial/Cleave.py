from erukar.system.engine import Attack, Damage, DamageScalar
from erukar.ext.math import Navigator


class Cleave(Attack):
    Name = 'Cleave'
    ShowInLists = True
    Description = 'Cleave with {} at {}'
    CurrentLevel = 'Swing wildly, inflicting {:0.1f}% damage per tile '\
        'in three spaces at once. Cleave uses two action points and '\
        'only rolls an attack once. Damage will hit in a in a 90 degree '\
        'arc centered on the specified space and will only hit hostile '\
        'creatures.'
    NextLevel = 'Increases percentage of damage per tile to {:0.1f}%.'
    OnSwing = 'You swing your {weapon} in the air wildly!'
    SeeSwing = '{attacker} swings its {weapon} wildly!'
    HitNothing = 'You fail to hit any target with your Cleave attack!'

    def ap_cost(self, *_):
        return 2

    def command(self, creature, weapon, loc):
        return {
            'command': 'ActivateAbility',
            'abilityModule': self.__module__,
            'cost': self.ap_cost(None, None),
            'description': self.format_description(creature, weapon, loc),
            'weapon': str(weapon.uuid),
            'interaction_target': loc,
        }

    def format_description(self, target, weapon, loc):
        return self.Description.format(weapon.alias(), loc)

    def valid_at(self, cmd, loc):
        player = cmd.args['player_lifeform']
        if player.action_points() < self.ap_cost(cmd, loc):
            return False
        if not any(Attack.weapons_in_range(player, loc)):
            return False
        return True

    def action_for_map(self, cmd, loc):
        player = cmd.args['player_lifeform']
        for weapon in Attack.weapons_in_range(player, loc):
            yield self.command(player, weapon, loc)

    def perform_attack(self, cmd, player, weapon, target):
        roll = self.calc_attack_roll(cmd, player, weapon, target)
        targets = list(self.affected_enemies(cmd))
        if len(targets) < 1:
            whoops = Cleave.HitNothing.format(weapon.alias())
            cmd.append_result(player.uid, whoops)
        for enemy in targets:
            self.perform_sub_attack(cmd, player, weapon, enemy, roll)
        return cmd.succeed()

    def calc_attack_roll(self, cmd, player, weapon, target):
        weapon.on_calculate_attack(cmd)
        roll = player.calculate_attack_roll(0.8, target)
        for mod in self.possible_modifiers:
            mod_name = 'modify_attack_roll'
            roll = mod.modify_element(mod_name, roll)
        return roll

    def affected_enemies(self, cmd):
        player = cmd.args['player_lifeform']
        at = cmd.args['interaction_target']
        for loc in self.affected_tiles(player, at):
            for enemy in cmd.world.creatures_at(player, loc):
                yield enemy

    def perform_sub_attack(self, cmd, player, weapon, enemy, roll):
        if not enemy.is_hostile_to(player):
            return
        hit = self.attack_succeeded(cmd, player, weapon, enemy, roll)
        if not hit:
            return
        self.do_damage(cmd, player, weapon, enemy)
        self.check_for_kill(cmd, player, weapon, enemy)

    def is_in_valid_range(self, player, weapon, target):
        dist = Navigator.distance(player.coordinates, target)
        return dist <= weapon.attack_range(player)

    def mit_carried_through(level):
        if level < 5:
            return 1.0
        return 1.0 - (level - 4) * 0.10

    def multiplier(level):
        if level > 4:
            return 1.0
        return 0.75 * 0.05*level

    def current_level_description(self):
        percent = Cleave.multiplier(self.level) * 100.0
        return self.CurrentLevel.format(percent)

    def next_level_description(self):
        percent = Cleave.multiplier(self.level + 1) * 100.0
        return self.NextLevel.format(percent)

    def affected_tiles(self, player, loc):
        p_x, p_y = player.coordinates
        x, y = loc
        if p_x == x:
            return Cleave.horizontal_tiles(p_x, y)
        if p_y == y:
            return Cleave.vertical_tiles(x, p_y)
        return Cleave.arc_tiles(x, y, p_x, p_y)

    def horizontal_tiles(x, y):
        return [(x-1, y), (x, y), (x+1, y)]

    def vertical_tiles(x, y):
        return [(x, y-1), (x, y), (x, y+1)]

    def arc_tiles(x, y, p_x, p_y):
        tiles = [(p_x, p_y)]
        # X Tiles
        tiles += [(p_x+1, p_y)] if x < p_x\
            else [(p_x-1, p_y)]
        # Y Tiles
        tiles += [(p_x, p_y+1)] if y < p_y\
            else [(p_x, p_y-1)]
        return tiles
