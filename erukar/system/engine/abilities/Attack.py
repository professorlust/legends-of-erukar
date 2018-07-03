from erukar.system.engine import TargetedAbility, Weapon
from erukar.system.engine import Corpse, Dying, Dead
from erukar.ext.math import Navigator


class Attack(TargetedAbility):
    Name = "Attack"
    ShowInLists = False
    Description = 'Attack {} with {}'
    NotFound = 'Could not find a valid target to attack.'
    NoWeapon = 'No valid weapon was specified.'
    NoAmmo = 'The appropriate ammo for this weapon is not equipped!'
    OutOfRange = 'Target is outside of maximum range!'
    NotEnoughAP = 'Not enough action points!'
    DidRoll = 'You swing your {weapon} at {target} with an attack roll '\
        'of {roll}...'
    RolledAt = '{attacker} swings a {weapon} at you with an attack roll '\
        'of {roll}...'
    Missed = '{target} moved too quickly, evading your attack! '\
        '({evasion} Evasion vs {roll} Attack Roll)'
    Dodged = 'You move faster than {attacker}\'s {weapon} and evade its '\
        '{weapon}! ({evasion} Evasion) vs {roll} Attack Roll)'
    DidHit = 'Your attack swings true!'
    GotHit = 'You can\'t dodge out of the way in time and are hit!'
    DealDamage = 'You deal {final} damage to {target}!'
    TakeDamage = 'You take {total} ({final}) damage.'
    DidNoDamage = 'Your attack deals no damage.'
    TakeNoDamage = 'Your armor mitigates all damage!'
    CauseDying = '{target} collapses, dying!'
    BecomeDying = 'You collapse and are now dying...'
    KillTarget = 'You have killed {target}!'
    BecomeKilled = 'You have been slain...'

    def valid_at(self, cmd, loc):
        player = cmd.args['player_lifeform']
        if player.action_points() < self.ap_cost(cmd, loc):
            return False
        for creature in cmd.world.creatures_at(player, loc):
            if creature.is_hostile_to(player):
                return Attack.has_weapons(player)
        return False

    def has_weapons(player):
        return any(Attack.valid_weapons(player))

    def action_for_map(self, cmd, loc):
        player = cmd.args['player_lifeform']
        for creature in cmd.world.creatures_at(player, loc):
            if not creature.is_hostile_to(player):
                continue
            for weapon in Attack.valid_weapons(player):
                yield self.command(creature, weapon, loc)

    def command(self, creature, weapon, loc):
        return {
            'command': 'ActivateAbility',
            'abilityModule': self.__module__,
            'cost': self.ap_cost(None, None),
            'description': self.format_description(creature, weapon, loc),
            'weapon': str(weapon.uuid),
            'interaction_target': str(creature.uuid)
        }

    def valid_weapons(player):
        if isinstance(player.left, Weapon):
            yield player.left
        if isinstance(player.right, Weapon):
            yield player.right

    def weapons_in_range(self, player, loc):
        dist = Navigator.distance(player.coordinates, loc)
        for weapon in Attack.valid_weapons(player):
            if dist <= weapon.attack_range(player):
                yield weapon

    def format_description(self, target, weapon, loc):
        return self.Description.format(target.alias(), weapon.alias())

    def perform(self, cmd):
        player = cmd.args['player_lifeform']
        target = cmd.args.get('interaction_target', None)
        weapon = cmd.args.get('weapon', None)

        failures = self.validate(cmd, player, target, weapon)
        if failures:
            return failures
        player.consume_action_points(self.ap_cost(cmd))
        self.possible_modifiers = [self, player, weapon]
        self.handle_ammo(cmd, player, weapon)
        result = self.perform_attack(cmd, player, weapon, target)
        self.possible_modifiers = []
        return result

    def perform_attack(self, cmd, player, weapon, target):
        roll = self.calc_attack_roll(cmd, player, weapon, target)
        if not self.attack_succeeded(cmd, player, weapon, target, roll):
            for modifier in self.possible_modifiers:
                modifier.post_missed_attack(cmd, player, weapon, target)
            return cmd.succeed()
        for modifier in self.possible_modifiers:
            modifier.post_successful_attack(cmd, player, weapon, target)
        return cmd.succeed()

    def post_successful_attack(self, cmd, player, weapon, target):
        self.do_damage(cmd, player, weapon, target)
        self.check_for_kill(cmd, player, weapon, target)

    def post_missed_attack(self, cmd, player, weapon, target):
        pass

    def can_activate(self):
        return True

    def ap_cost(self, *_):
        return 1

    def validate(self, cmd, player, target, weapon):
        if not target:
            return cmd.fail(Attack.NotFound)
        if not weapon or not self.weapon_exists(player, weapon):
            return cmd.fail(Attack.NoWeapon)

        failed_requirements = weapon.failing_requirements(player)
        if failed_requirements:
            return cmd.fail('. '.join(failed_requirements))
        if not self.has_ammo_if_needed(player, weapon):
            return cmd.fail(Attack.NoAmmo)
        if not self.is_in_valid_range(player, weapon, target):
            return cmd.fail(Attack.OutOfRange)

        cost = self.ap_cost(cmd)
        if player.action_points() < cost:
            return cmd.fail(Attack.NotEnoughAP)

    def weapon_exists(self, player, weapon):
        return isinstance(weapon, Weapon)\
                and (player.left == weapon or player.right == weapon)

    def has_ammo_if_needed(self, player, weapon):
        '''Do we consume ammo and have the right ammo?'''
        return not weapon.RequiresAmmo\
            or weapon.has_correct_ammo(player.ammunition)

    def is_in_valid_range(self, player, weapon, target):
        dist = Navigator.distance(player.coordinates, target.coordinates)
        return dist <= weapon.attack_range(player)

    def handle_ammo(self, cmd, player, weapon):
        if not weapon.RequiresAmmo:
            return
        ammo = player.ammunition
        ammo.consume()
        self.possible_modifiers.append(ammo)

    def calc_attack_roll(self, cmd, player, weapon, target):
        weapon.on_calculate_attack(cmd)
        roll = player.calculate_attack_roll(1.0, target)
        for mod in self.possible_modifiers:
            mod_name = 'modify_attack_roll'
            roll = mod.modify_element(mod_name, roll)
        strings = {
            'attacker': player.alias(),
            'roll': roll,
            'weapon': weapon.alias(),
            'target': target.alias()
        }
        cmd.append_result(player.uid, Attack.DidRoll.format(**strings))
        cmd.append_result(target.uid, Attack.RolledAt.format(**strings))
        return roll

    def attack_succeeded(self, cmd, player, weapon, target, roll):
        roll = target.on_check_for_hit(player, weapon, roll)
        evasion = target.evasion()
        strings = {
            'attacker': player.alias(),
            'target': target.alias(),
            'weapon': weapon.alias(),
            'roll': roll,
            'evasion': evasion,
        }
        if roll <= evasion:
            target.on_successful_dodge(player, weapon, roll)
            player.on_missed_attack(target, weapon, roll)
            cmd.append_result(player.uid, self.Missed.format(**strings))
            cmd.append_result(target.uid, self.Dodged.format(**strings))
            return False
        target.on_failed_dodge(player, weapon, roll)
        player.on_successful_attack(target, weapon, roll)
        cmd.append_result(player.uid, self.DidHit.format(**strings))
        cmd.append_result(target.uid, self.GotHit.format(**strings))
        return True

    def do_damage(self, cmd, player, weapon, target):
        damage = player.get_damage_from_attack(target, weapon)
        for modifier in self.possible_modifiers:
            damage = modifier.modify_element('modify_damage', damage)
        result = target.apply_damage(player, weapon, damage)
        Attack.append_post_damage_strings(cmd, player, weapon, target, result)

    def final_damages(result):
        res = ['{} {}'.format(*x) for x in result['post_mitigation']]
        return ', '.join(res)

    def mitigated(result):
        return '[[mitigated]]'

    def deflected(result):
        return '[[deflected]]'

    def total(result):
        return result['total']

    def append_post_damage_strings(cmd, player, weapon, target, result):
        strs = {
            'attacker': player.alias(),
            'weapon': weapon.alias(),
            'target': target.alias(),
            'final': Attack.final_damages(result),
            'mitigated': Attack.mitigated(result),
            'deflected': Attack.deflected(result),
            'total': Attack.total(result)
        }
        if Attack.total(result) <= 0:
            cmd.append_result(player.uid, Attack.DidNoDamage.format(**strs))
            cmd.append_result(target.uid, Attack.TakeNoDamage.format(**strs))
            return
        cmd.dirty(player)
        cmd.dirty(target)
        cmd.append_result(player.uid, Attack.DealDamage.format(**strs))
        cmd.append_result(target.uid, Attack.TakeDamage.format(**strs))

    def check_for_kill(self, cmd, player, weapon, target):
        strs = {
            'attacker': player.alias(),
            'weapon': weapon.alias(),
            'target': target.alias(),
        }
        if target.has_condition(Dying):
            cmd.append_result(player.uid, Attack.CauseDying.format(**strs))
            cmd.append_result(target.uid, Attack.BecomeDying.format(**strs))
            return
        if target.has_condition(Dead):
            cmd.append_result(player.uid, Attack.KillTarget.format(**strs))
            cmd.append_result(target.uid, Attack.BecomeKilled.format(**strs))
            Attack.corpsify(cmd, player, target)
            weapon.on_kill(player, target)

    def corpsify(cmd, player, target):
        cmd.world.remove_actor(target)
        corpse = Corpse(target)
        cmd.world.add_actor(corpse, target.coordinates)
        xp = target.calculate_xp_worth()
        player.award_xp(xp, cmd)
