from erukar.system.engine import TargetedAbility, Weapon, PlayerNode
from erukar.system.engine import Corpse, Dying, Dead, Damage
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
    YouHit = 'You hit {target} with your {weapon} ({roll} attack), dealing '\
        '{report}'
    YouHitNoDamage = 'You hit {target} with your {weapon} ({roll} attack), '\
        'but deal no damage.{protections}'
    YouCauseDying = '{target} slumps to the ground, dying!'
    YouCauseDead = 'You have killed {target}!'
    YouMiss = '{target} dodges your {weapon} attack ({roll} attack).'
    YouAreHit = '{attacker} hits you with its {weapon} ({roll} attack), '\
        'dealing {report}'
    YouAreHitNoDamage = '{attacker} hits you with its {weapon} ({roll} '\
        'attack), but you take no damage.{protections}'
    YouAreMissed = 'You evade {attacker}\'s {weapon} attack ({roll} attack).'
    YouAreDying = 'You fall to the ground dying!'
    YouAreDead = 'You have died...'
    SeeHit = '{attacker} hits {target} with its {weapon} ({roll} attack), '\
        'dealing {final} damage.'
    SeeHitNoDamage = '{attacker} hits {target} with its {weapon} ({roll} '\
        'attack), but it does no damage.'
    SeeMiss = '{attacker} misses {target} with its {weapon} ({roll} attack).'
    SeeDying = '{target} slumps to the ground, dying.'
    SeeDead = '{target} has died.'
    VerboseDamageFormat = '{deflected}/{mitigated}/{final} {_type}'
    VerboseDamageReport = '{total} damage ({verbose_report})'
    ShortDamageReport = '{total} damage'

    def __init__(self):
        super().__init__()
        self.roll = 0

    def valid_at(self, cmd, loc):
        player = cmd.args['player_lifeform']
        if player.action_points() < Attack.ap_cost(cmd, loc):
            return False
        return Attack._valid_at(player, cmd.world, loc)

    def _valid_at(player, world, loc):
        for creature in world.creatures_at(player, loc):
            if creature.is_hostile_to(player):
                dist = Navigator.distance(player.coordinates, loc)
                return Attack.has_weapons(player, dist)
        return False

    def has_weapons(player, dist=0):
        return any(Attack.valid_weapons(player, dist))

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
            'cost': Attack.ap_cost(None, None),
            'description': self.format_description(creature, weapon, loc),
            'weapon': str(weapon.uuid),
            'interaction_target': str(creature.uuid)
        }

    def valid_weapons(player, dist=0):
        for item in [player.left, player.right]:
            if isinstance(item, Weapon):
                if item.attack_range(player) >= dist:
                    yield item

    def weapons_in_range(player, loc):
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
        player.consume_action_points(Attack.ap_cost(cmd))
        self.possible_modifiers = [self, player]
        self.handle_ammo(cmd, player, weapon)
        result = self.perform_attack(cmd, player, weapon, target)
        self.possible_modifiers = []
        return result

    def perform_attack(self, cmd, player, weapon, target):
        self.roll = self.calc_attack_roll(cmd, player, weapon, target)
        if not self.attack_succeeded(cmd, player, weapon, target):
            self.log_miss(cmd, player, weapon, target)
            for modifier in self.possible_modifiers:
                modifier.post_missed_attack(cmd, player, weapon, target)
            return cmd.succeed()
        for modifier in self.possible_modifiers:
            modifier.post_successful_attack(cmd, player, weapon, target)
        return cmd.succeed()

    def log_miss(self, cmd, player, weapon, target):
        args = {
            'attacker': player.alias(),
            'target': target.alias(),
            'weapon': weapon.alias(),
            'roll': self.roll
        }
        cmd.log(player, self.YouMiss.format(**args))
        cmd.log(target, self.YouAreMissed.format(**args))
        cmd.obs(
            target.coordinates,
            self.SeeMiss.format(**args),
            exclude=[player, target]
        )

    def post_successful_attack(self, cmd, player, weapon, target):
        self.do_damage(cmd, player, weapon, target)
        self.check_for_kill(cmd, player, weapon, target)

    def post_missed_attack(self, cmd, player, weapon, target):
        pass

    def can_activate(self):
        return True

    def ap_cost(*_):
        return 1

    def validate(self, cmd, player, target, weapon):
        if not target:
            return cmd.fail(Attack.NotFound)
        if not weapon or not Attack.weapon_exists(player, weapon):
            return cmd.fail(Attack.NoWeapon)

        failed_requirements = weapon.failing_requirements(player)
        if failed_requirements:
            return cmd.fail('. '.join(failed_requirements))
        if not Attack.has_ammo_if_needed(player, weapon):
            return cmd.fail(Attack.NoAmmo)
        if not Attack.is_in_valid_range(player, weapon, target):
            return cmd.fail(Attack.OutOfRange)

        cost = Attack.ap_cost(cmd)
        if player.action_points() < cost:
            return cmd.fail(Attack.NotEnoughAP)

    def weapon_exists(player, weapon):
        return isinstance(weapon, Weapon)\
                and (player.left == weapon or player.right == weapon)

    def has_ammo_if_needed(player, weapon):
        '''Do we consume ammo and have the right ammo?'''
        return not weapon.RequiresAmmo\
            or weapon.has_correct_ammo(player.ammunition)

    def is_in_valid_range(player, weapon, target):
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
            roll = mod.modify_element(mod_name, roll, cmd)
        return roll

    def attack_succeeded(self, cmd, player, weapon, target):
        self.roll = target.on_check_for_hit(player, weapon, self.roll)
        if self.roll <= target.evasion():
            target.on_successful_dodge(player, weapon, self.roll)
            player.on_missed_attack(target, weapon, self.roll)
            return False
        target.on_failed_dodge(player, weapon, self.roll)
        player.on_successful_attack(target, weapon, self.roll)
        return True

    def do_damage(self, cmd, player, weapon, target):
        damage = player.get_damage_from_attack(target, weapon)
        for modifier in self.possible_modifiers:
            damage = modifier.modify_element('modify_damage', damage, cmd)
        result = target.apply_damage(player, weapon, damage)
        self.append_post_damage_strings(cmd, player, weapon, target, result)

    def final_damages(result):
        return ', '.join(Damage.ordered(result['post_mitigation']))

    def mitigated(result):
        _total = {k: v for k, v in Attack._mitigation(result)}
        return ', '.join(Damage.ordered(_total))

    def _mitigation(result):
        for _type in result['post_deflection']:
            pre = result['post_deflection'][_type]
            post = result['post_mitigation'].get(_type, 0)
            if post < pre:
                yield _type, (pre - post)

    def deflected(result):
        _total = {k: v for k, v in Attack._deflected(result)}
        return ', '.join(Damage.ordered(_total))

    def _deflected(result):
        for _type in result['raw']:
            pre = result['raw'][_type]
            post = result['post_deflection'].get(_type, 0)
            if post < pre:
                yield _type, (pre - post)

    def total(result):
        return result['total']

    def protections(result):
        dfl = Attack.deflected(result)
        mit = Attack.mitigated(result)
        dfl = '' if not dfl else '{} deflected'.format(dfl)
        mit = '' if not mit else '{} mitigated'.format(mit)
        protections = ', '.join(x for x in [dfl, mit] if x)
        return '' if not protections else ' ({})'.format(protections)

    def append_post_damage_strings(self, cmd, player, weapon, target, result):
        strs = {
            'attacker': player.alias(),
            'weapon': weapon.alias(),
            'target': target.alias(),
            'final': result['total'],
            'total': Attack.total(result),
            'roll': self.roll,
            'protections': Attack.protections(result),
            'report': Attack.assemble_report(player, result)
        }
        if Attack.total(result) <= 0:
            Attack.log_no_damage(cmd, player, target, strs)
            return
        cmd.dirty(player)
        cmd.dirty(target)
        Attack.log_damage(cmd, player, target, strs)

    def assemble_report(player, result):
        if not isinstance(player, PlayerNode) or not player.verbose_log:
            return Attack.ShortDamageReport.format(total=result['total'])
        reports = []
        for _type in [*result['raw']]:
            final = int(result['post_mitigation'].get(_type, 0))
            mit = int(result['post_deflection'].get(_type, 0) - final)
            dfl = int(result['raw'].get(_type, 0) - mit)
            _report = Attack.VerboseDamageFormat.format(
                deflected=dfl,
                mitigated=mit,
                final=final,
                _type=_type
            )
            reports.append(_report)
        args['report'] = ', '.join(reports)
        return Attack.VerboseDamageReport.format(**args)

    def log_no_damage(cmd, player, target, args):
        cmd.log(player, Attack.YouHitNoDamage.format(**args))
        cmd.log(target, Attack.YouAreHitNoDamage.format(**args))
        cmd.obs(
            target.coordinates,
            Attack.SeeHitNoDamage.format(**args),
            exclude=[player, target]
        )

    def log_damage(cmd, player, target, args):
        cmd.log(player, Attack.YouHit.format(**args))
        cmd.log(target, Attack.YouAreHit.format(**args))
        cmd.obs(
            target.coordinates,
            Attack.SeeHit.format(**args),
            exclude=[player, target]
        )

    def check_for_kill(self, cmd, player, weapon, target):
        strs = {
            'attacker': player.alias(),
            'weapon': weapon.alias(),
            'target': target.alias(),
        }
        if target.has_condition(Dying):
            cmd.log(player, Attack.YouCauseDying.format(**strs))
            cmd.log(target, Attack.YouAreDying.format(**strs))
            cmd.obs(
                target.coordinates,
                self.SeeDying.format(**strs),
                exclude=[player, target]
            )
            return
        if target.has_condition(Dead):
            cmd.log(player, Attack.YouCauseDead.format(**strs))
            cmd.log(target, Attack.YouAreDead.format(**strs))
            cmd.obs(
                target.coordinates,
                self.SeeDead.format(**strs),
                exclude=[player, target]
            )
            Attack.corpsify(cmd, player, target)
            weapon.on_kill(player, target)

    def corpsify(cmd, player, target):
        cmd.world.remove_actor(target)
        corpse = Corpse(target)
        cmd.world.add_actor(corpse, target.coordinates)
        xp = target.calculate_xp_worth()
        player.award_xp(xp, cmd)

    def post_inflict_damage(self, cmd):
        pass
